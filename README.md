# Health Check AI with Integrated Health Profiling

This project integrates a deep convolutional neural network (CNN) trained from scratch with a Streamlit front-end for predicting food calories and giving personalized dietary advice based on BMI.

## Project Structure
- `requirements.txt`: Dependencies for the Streamlit deployment.
- `kaggle_train.py`: Script to train the model on Kaggle using Multi-GPU.
- `app.py`: The Streamlit web application.

## Deployment Steps

### Step 1: Run the Training Script on Kaggle
1. Go to [Kaggle](https://www.kaggle.com/) and create a new Notebook.
2. Add your dataset (e.g., Food-101 or a custom 10-class dataset).
3. Under Notebook settings, select **Accelerator > GPU T4 x2**.
4. Upload `kaggle_train.py` or copy-paste its content into the notebook cells.
5. Make sure to update the `DATASET_PATH` inside the script to point to your dataset directory.
6. Run the script to train the model using Multi-GPU strategy.

### Step 2: Download the `.keras` File
1. Once training is complete, Kaggle will save `heavy_custom_food_model.keras` to the working output directory.
2. Download this file to your local machine from the Kaggle Data/Output panel on the right sidebar.

### Step 3: Upload Files to GitHub
1. Create a new public repository on [GitHub](https://github.com/).
2. Upload the following files to the root directory of your repository:
   - `app.py`
   - `requirements.txt`
   - `heavy_custom_food_model.keras`
3. Commit and push the changes.

### Step 4: Link to Streamlit Community Cloud
1. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **New app**.
3. Select your repository, branch, and set the **Main file path** to `app.py`.
4. Click **Deploy!**
5. Streamlit will install the lightweight `tensorflow-cpu` from `requirements.txt` and launch your application.
