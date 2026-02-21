import os
from services import training_service

def train_model(model_type, file_path):
    if not os.path.exists(file_path): return False, "File not found."
    try:
        if model_type == "Text Analysis (SMS/Spam)":
            if training_service.train_text_model(file_path): return True, "NLP Model successfully trained and deployed."
            return False, "Failed to train Text Model."
        elif model_type == "Audio Analysis (Deepfake/Voice)":
            if training_service.train_audio_model(file_path): return True, "Audio Model successfully trained and deployed."
            return False, "Failed to train Audio Model."
    except Exception as e:
        return False, str(e)