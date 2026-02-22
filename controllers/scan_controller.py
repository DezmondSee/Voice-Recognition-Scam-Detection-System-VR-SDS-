import joblib
from services.audio_processor import extract_features
from config.db_config import get_db_connection

def load_model(path):
    try: return joblib.load(path)
    except: return None

def process_audio(user_id, file_path):
    model = load_model("models/scam_detector.pkl")
    if not model: return {"error": "AI Engine Offline. Admin must train model."}
    
    features = extract_features(file_path)
    if features is None: return {"error": "Invalid Audio File"}
    
    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features).max() * 100
    verdict = "SCAM" if prediction == 1 else "SAFE"
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO call_logs (user_id, scan_type, verdict, confidence) VALUES (%s, 'AUDIO', %s, %s)", (user_id, verdict, confidence))
        conn.commit()
        conn.close()
    return {"verdict": verdict, "confidence": round(confidence, 2)}

def process_text(user_id, text_input):
    model = load_model("models/text_scam_detector.pkl")
    if not model: return {"error": "AI Engine Offline. Admin must train model."}
    
    prediction = model.predict([text_input])[0]
    verdict = "SCAM" if prediction == 1 else "SAFE"
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO call_logs (user_id, scan_type, verdict, confidence) VALUES (%s, 'TEXT', %s, 95.0)", (user_id, verdict))
        conn.commit()
        conn.close()
    return {"verdict": verdict}