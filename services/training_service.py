import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split

os.makedirs("models", exist_ok=True)

def train_text_model(csv_path):
    try:
        df = pd.read_csv(csv_path)
        if 'Message' in df.columns: df = df.rename(columns={'Message': 'text', 'Category': 'label'})
        df['label'] = df['label'].astype(int)
        
        X_train, _, y_train, _ = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)
        model = make_pipeline(TfidfVectorizer(), RandomForestClassifier(n_estimators=100, random_state=42))
        model.fit(X_train, y_train)
        joblib.dump(model, "models/text_scam_detector.pkl")
        return True
    except Exception as e:
        print(f"Text Training Error: {e}")
        return False

def train_audio_model(csv_path):
    try:
        df = pd.read_csv(csv_path)
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values.astype(int)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        joblib.dump(model, "models/scam_detector.pkl")
        return True
    except Exception as e:
        print(f"Audio Training Error: {e}")
        return False