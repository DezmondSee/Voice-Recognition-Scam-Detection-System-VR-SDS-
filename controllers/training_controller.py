import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

MODEL_DIR = "models"

def train_model(model_type, dataset_path=""):
    """Trains or updates AI models using REAL datasets and persists them to the models/ folder."""
    try:
        os.makedirs(MODEL_DIR, exist_ok=True)
        
        # ---------------------------------------------------------
        # 1. TEXT MODEL LOGIC (Safe Bypass)
        # ---------------------------------------------------------
        if "Text" in model_type:
            # You already have the pre-trained text_scam_detector.pkl and text_vectorizer.pkl
            # This prevents the app from accidentally overwriting your good text models.
            return True, "Text models are already pre-trained and actively running from the models/ folder."
        
        # ---------------------------------------------------------
        # 2. AUDIO MODEL LOGIC (Real Dataset Training)
        # ---------------------------------------------------------
        filename = "scam_detector.pkl"
        save_path = os.path.join(MODEL_DIR, filename)
        
        # Define the paths to your real dataset files
        x_file = "X.npy"
        y_file = "y.npy"
        
        # Safety check: Ensure the files actually exist where the script is running
        if not os.path.exists(x_file) or not os.path.exists(y_file):
            return False, f"Dataset missing! Please ensure '{x_file}' and '{y_file}' are placed in the root project folder."
            
        # Load the real extracted audio features and labels
        X = np.load(x_file)
        y = np.load(y_file)
        
        # Initialize and train the actual Random Forest brain
        # n_estimators=100 ensures a robust forest, random_state keeps results reproducible
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X, y)
        
        # Save the newly trained real model to the models directory
        joblib.dump(clf, save_path)
        
        return True, f"Audio Model successfully trained on {X.shape[0]} samples (with {X.shape[1]} features each) and saved to {save_path}!"
        
    except Exception as e:
        return False, f"Training failed: {str(e)}"