import tensorflow as tf
import os
import pathlib

import tensorflow as tf
import os

# 1. Point directly to your attached Kaggle input datasets
DATASET_PATHS = [
    "/kaggle/input/datasets/dansbecker/food-101",
    "/kaggle/input/datasets/iamsouravbanerjee/indian-food-images-dataset"
]

valid_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

all_file_paths = []
class_names_set = set()

# Scan through both datasets
for dataset_path in DATASET_PATHS:
    if os.path.exists(dataset_path):
        for root, dirs, files in os.walk(dataset_path):
            for f in files:
                if f.lower().endswith(valid_exts):
                    full_p = os.path.join(root, f)
                    all_file_paths.append(full_p)
                    
                    # Class name is the immediate parent folder
                    parent_folder = os.path.basename(root)
                    if parent_folder not in [os.path.basename(p) for p in DATASET_PATHS]:
                        class_names_set.add(parent_folder)

class_names = sorted(list(class_names_set))
num_classes = len(class_names)

print(f"Detected {len(all_file_paths)} valid images across {num_classes} classes!")

# Check if images were found (using DATASET_PATHS correctly here)
if num_classes == 0:
    raise ValueError(f"No image files found in {DATASET_PATHS}. Please verify dataset paths under /kaggle/input/!")

class_to_idx = {name: idx for idx, name in enumerate(class_names)}
labels = [class_to_idx[os.path.basename(os.path.dirname(p))] for p in all_file_paths]


# 2. Build TF Dataset
path_ds = tf.data.Dataset.from_tensor_slices((all_file_paths, labels))

def load_and_preprocess_image(path):
    image_bytes = tf.io.read_file(path)
    image = tf.io.decode_image(image_bytes, channels=3, expand_animations=False)
    image = tf.image.resize(image, [224, 224])
    return image

def process_path(path, label):
    image = tf.py_function(
        func=lambda p: load_and_preprocess_image(p.numpy().decode('utf-8')),
        inp=[path],
        Tout=tf.float32
    )
    image.set_shape([224, 224, 3])
    return image, label

full_ds = path_ds.map(process_path, num_parallel_calls=tf.data.AUTOTUNE).ignore_errors()

# 3. Train / Val Split (Clean & Safe)
total_count = len(all_file_paths)
val_size = int(total_count * 0.2)

# Create train and validation path lists explicitly upfront
train_paths, train_labels = all_file_paths[val_size:], labels[val_size:]
val_paths, val_labels = all_file_paths[:val_size], labels[:val_size]

def create_dataset(paths, labels, batch_size=32):
    ds = tf.data.Dataset.from_tensor_slices((paths, labels))
    ds = ds.map(process_path, num_parallel_calls=tf.data.AUTOTUNE).ignore_errors()
    return ds.batch(batch_size).prefetch(buffer_size=tf.data.AUTOTUNE)

train_ds = create_dataset(train_paths, train_labels)
val_ds = create_dataset(val_paths, val_labels)


import random

# 1. Zip the paths and labels together so they shuffle perfectly in sync
combined_data = list(zip(all_file_paths, labels))
random.shuffle(combined_data)

# 2. Unzip them back into two lists
shuffled_paths, shuffled_labels = zip(*combined_data)
shuffled_paths = list(shuffled_paths)
shuffled_labels = list(shuffled_labels)

# 3. NOW do the 80/20 Split on the properly mixed data
total_count = len(shuffled_paths)
val_size = int(total_count * 0.2)

train_paths = shuffled_paths[val_size:]
train_labels = shuffled_labels[val_size:]

val_paths = shuffled_paths[:val_size]
val_labels = shuffled_labels[:val_size]

print(f"Data properly shuffled! Train size: {len(train_paths)}, Val size: {len(val_paths)}")


import tensorflow as tf
import os

# 1. Helper functions to encode data into binary
def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def create_tfrecord(image_path, label):
    # Read raw bytes directly
    image_string = tf.io.read_file(image_path)
    feature = {
        'image_raw': _bytes_feature(image_string.numpy()),
        'label': _int64_feature(label)
    }
    tf_example = tf.train.Example(features=tf.train.Features(feature=feature))
    return tf_example.SerializeToString()

# 2. Write the dataset into Sharded TFRecords
def write_sharded_tfrecords(paths, labels, out_dir, prefix, shard_size=2000):
    os.makedirs(out_dir, exist_ok=True)
    num_samples = len(paths)
    num_shards = (num_samples // shard_size) + 1
    print(f"Creating {num_shards} shards for {prefix} data...")
    
    for shard in range(num_shards):
        start_idx = shard * shard_size
        end_idx = min((shard + 1) * shard_size, num_samples)
        
        if start_idx >= num_samples:
            break
            
        record_file = os.path.join(out_dir, f'{prefix}_shard_{shard:03d}.tfrec')
        with tf.io.TFRecordWriter(record_file) as writer:
            for i in range(start_idx, end_idx):
                writer.write(create_tfrecord(paths[i], labels[i]))
        print(f"Saved {record_file} ({end_idx - start_idx} images)")

# RUN IT! (Assuming your lists are named train_paths, train_labels, etc.)
print("Converting Training Data...")
write_sharded_tfrecords(train_paths, train_labels, '/kaggle/working/tfrecords/', 'train')

print("\nConverting Validation Data...")
write_sharded_tfrecords(val_paths, val_labels, '/kaggle/working/tfrecords/', 'val')



def parse_tfrecord(example_proto):
    feature_description = {
        'image_raw': tf.io.FixedLenFeature([], tf.string),
        'label': tf.io.FixedLenFeature([], tf.int64),
    }
    parsed_example = tf.io.parse_single_example(example_proto, feature_description)
    
    image = tf.io.decode_image(parsed_example['image_raw'], channels=3, expand_animations=False)
    image.set_shape([None, None, 3]) 
    image = tf.image.resize(image, [224, 224])
    label = parsed_example['label']
    return image, label

def get_fast_dataset(tfrecord_pattern, batch_size=64, is_training=False):
    files = tf.data.Dataset.list_files(tfrecord_pattern)
    dataset = files.interleave(
        tf.data.TFRecordDataset, 
        cycle_length=tf.data.AUTOTUNE, 
        num_parallel_calls=tf.data.AUTOTUNE
    )
    
    dataset = dataset.map(parse_tfrecord, num_parallel_calls=tf.data.AUTOTUNE).ignore_errors()
    
    # CRITICAL FIX: Add .repeat() so Keras never runs out of data unexpectedly
    if is_training:
        dataset = dataset.shuffle(8192).repeat()
    else:
        dataset = dataset.repeat() # Validation needs to loop too
        
    dataset = dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)
    return dataset

# Initialize the updated datasets
fast_train_ds = get_fast_dataset('/kaggle/working/tfrecords/train_*.tfrec', batch_size=64, is_training=True)
fast_val_ds = get_fast_dataset('/kaggle/working/tfrecords/val_*.tfrec', batch_size=64, is_training=False)
print("Pipelines on infinite loop and ready!")


import tensorflow as tf

# Calculate exact steps per epoch so Keras knows when to stop
# Total Train = 164,800 | Total Val = 41,200 | Batch Size = 64
TRAIN_STEPS = 164800 // 64
VAL_STEPS = 41200 // 64

# 1. Load the Heavy Hitter: EfficientNetV2S
base_model = tf.keras.applications.EfficientNetV2S(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False

model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(181, activation='softmax')
])

# Phase 1: Warm up
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)

print("🚀 Retraining Phase 1: EfficientNetV2S (Frozen Base)...")
model.fit(
    fast_train_ds, 
    validation_data=fast_val_ds, 
    epochs=5,
    steps_per_epoch=TRAIN_STEPS,     # Tell Keras exactly when to stop!
    validation_steps=VAL_STEPS,      # Tell Keras exactly when to stop!
    callbacks=[tf.keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.5, patience=1)]
)

print("🔥 Phase 1 Complete! Unfreezing the Beast for Phase 2...")

# Phase 2: Fine-Tune
model.layers[0].trainable = True
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4), 
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)

model.fit(
    fast_train_ds,
    validation_data=fast_val_ds,
    epochs=15, 
    steps_per_epoch=TRAIN_STEPS,     # Tell Keras exactly when to stop!
    validation_steps=VAL_STEPS,      # Tell Keras exactly when to stop!
    callbacks=[
        tf.keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.5, patience=2, min_lr=1e-6)
    ]
)

model.save("efficientnet_v2s_food_model_ULTIMATE.keras")
print("✅ EfficientNetV2S model saved. Now THAT is a real model!")