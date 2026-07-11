import streamlit as tf_streamlit_app
import tensorflow as tf
import numpy as np
import pickle
from PIL import Image

# Set up page configuration
tf_streamlit_app.set_page_config(page_title="🍏 Calorie & Health Check AI", layout="wide")

# ----------------------------------------------------
# 1. LOAD CONFIGURATIONS & MODELS
# ----------------------------------------------------
@tf_streamlit_app.cache_resource
def load_ai_components():
    # Load the trained 20-class Indian food model
    model = tf.keras.models.load_model('indian_food_model.keras')
    
    # Load the calorie mapping dictionary from the pickle file
    with open('calorie_dict.pkl', 'rb') as f:
        calorie_mapping = pickle.load(f)
        
    # Reconstruct class names directly from the dictionary keys
    categories = list(calorie_mapping.keys())
    return model, calorie_mapping, categories

try:
    food_model, calorie_dict, class_names = load_ai_components()
except Exception as e:
    tf_streamlit_app.error("⚠️ Make sure 'indian_food_model.keras' and 'calorie_dict.pkl' are in the same folder as this script!")

# ----------------------------------------------------
# 2. APP HEADER & LAYOUT
# ----------------------------------------------------
tf_streamlit_app.title("🍏 Calorie Scanner & Health Advisor AI")
tf_streamlit_app.markdown("Upload a photo of your Indian meal for an instant calorie breakdown, and calculate your BMI for personalized dietary guidance.")
tf_streamlit_app.write("---")

col1, col2 = tf_streamlit_app.columns([1, 1])

# ----------------------------------------------------
# LEFT COLUMN: FOOD RECOGNITION & CALORIES
# ----------------------------------------------------
with col1:
    tf_streamlit_app.header("📸 Scan Your Food")
    uploaded_file = tf_streamlit_app.file_uploader("Choose a food image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        tf_streamlit_app.image(image, caption="Uploaded Food Image", use_container_width=True)
        
        # Preprocess the image to match MobileNetV2 expectations
        img_resized = image.resize((224, 224))
        img_array = np.array(img_resized)
        
        # Handle cases where PNG images might have an alpha channel (RGBA)
        if img_array.shape[-1] == 4:
            img_array = img_array[..., :3]
            
        # Normalize and add batch dimension
        img_scaled = img_array / 255.0
        img_batch = np.expand_dims(img_scaled, axis=0)
        
        with tf_streamlit_app.spinner("Analyzing meal contents..."):
            predictions = food_model.predict(img_batch)
            pred_idx = np.argmax(predictions[0])
            predicted_food = class_names[pred_idx]
            confidence = predictions[0][pred_idx] * 100
            
        # Display analysis results
        tf_streamlit_app.success(f"**Identified Dish:** {predicted_food.replace('_', ' ')} ({confidence:.1f}% confidence)")
        
        # Fetch calories per serving (or 100g baseline)
        base_calories = calorie_dict.get(predicted_food, 250)
        tf_streamlit_app.metric(label="Estimated Energy Content", value=f"{base_calories} kcal", delta="Per serving baseline")

# ----------------------------------------------------
# RIGHT COLUMN: BMI CALCULATOR & DIET ADVISOR
# ----------------------------------------------------
with col2:
    tf_streamlit_app.header("⚖️ BMI & Diet Profiler")
    
    # Input sliders for physical metrics
    weight = tf_streamlit_app.number_input("Weight (in kg)", min_value=10.0, max_value=200.0, value=65.0, step=0.5)
    height_cm = tf_streamlit_app.number_input("Height (in cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.5)
    
    if tf_streamlit_app.button("Calculate Health Report"):
        # Calculate BMI: weight (kg) / height (m)^2
        height_m = height_cm / 100.0
        bmi = weight / (height_m ** 2)
        
        tf_streamlit_app.subheader(f"Your Calculated BMI: **{bmi:.1f}**")
        
        # Stratify recommendations according to BMI status
        if bmi < 18.5:
            tf_streamlit_app.warning("Classification: **Underweight**")
            tf_streamlit_app.markdown("""
            ### 🥦 Recommended Strategy (Weight Gain Focus):
            * **Caloric Surplus:** Target energy-dense but nutritious meals.
            * **Dietary Enhancements:** Integrate healthy fats like nuts, seeds, ghee, paneer, and avocados.
            * **Macronutrient Balance:** Increase protein intake (pulses, sprouts, dairy) alongside complex carbohydrates (rice, chapathi) to assist muscular growth.
            """)
        elif 18.5 <= bmi < 24.9:
            tf_streamlit_app.success("Classification: **Normal / Healthy Weight**")
            tf_streamlit_app.markdown("""
            ### 🥗 Recommended Strategy (Maintenance Focus):
            * **Balanced Nutrition:** Maintain a diverse, clean diet containing an even spread of macronutrients.
            * **Portion Control:** Keep enjoying regional items like Dal, Sabzi, Poha, and Idli while avoiding excessive fried street variants.
            * **Hydration:** Ensure consistent water intake alongside high-fiber leafy greens.
            """)
        elif 24.9 <= bmi < 29.9:
            tf_streamlit_app.info("Classification: **Overweight**")
            tf_streamlit_app.markdown("""
            ### 🏃‍♂️ Recommended Strategy (Caloric Deficit Focus):
            * **Fiber Optimization:** Increase consumption of whole grains, raw vegetables, oats, and salads.
            * **Refined Reduction:** Minimize intake of heavy carbohydrates and sugars (limit white rice, high-glycemic items, and fried deep snacks like Samosas/Vada Pav).
            * **Lean Alternatives:** Opt for Besan Cheela, sprouts, grilled paneer, and boiled lentils over calorie-dense curries.
            """)
        else:
            tf_streamlit_app.error("Classification: **Obese**")
            tf_streamlit_app.markdown("""
            ### 🩺 Recommended Strategy (Structured Management):
            * **Professional Alignment:** Highly advisable to pair these guidelines with a certified medical nutritionist.
            * **Sugar & Oil Cessation:** Significantly lower visible oils, butter, refined sugars, and ultra-processed fast items.
            * **Nutrient Density:** Structure major meals around high-volume, low-calorie foods like clear soups, mixed vegetables, buttermilk, and protein-packed pulses.
            """)
