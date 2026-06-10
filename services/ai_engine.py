import librosa
import numpy as np
import speech_recognition as sr
import os
import joblib
import soundfile as sf
import tempfile
import scipy.signal
import scipy.signal.windows
import spacy
import spacy.cli

# Fix for librosa/scipy compatibility on some environments
if not hasattr(scipy.signal, 'hann'):
    scipy.signal.hann = scipy.signal.windows.hann

# --- MODEL PATHS ---
AUDIO_MODEL_PATH = "models/scam_detector.pkl"
TEXT_MODEL_PIPELINE_PATH = "models/text_scam_detector.pkl"

# --- THE UNIVERSAL MALAYSIAN SCAM MATRIX ---
MALAYSIAN_SCAM_PATTERNS = {
    "authorities": [
        "lhdn", "pdrm", "mcmc", "kastam", "customs", "mahkamah", "court", 
        "pos laju", "jnt", "income tax", "sprm", "bank negara", "bnm", "polis", "balai"
    ],
    "financial": [
        "credit card", "underwriting", "account", "bank", "maybank", "cimb", 
        "ambank", "public bank", "rhb", "hong leong", "rm", "tac", "mule", "transfer", "cvv", "pin"
    ],
    "urgency_and_threats": [
        "3 business days", "immediately", "urgent", "now", "deadline", 
        "suspended", "blocked", "attention", "warrant", "arrest", "police report", 
        "legal action", "illegal activities", "freeze", "blacklist", "saman", "penalty", "penjara"
    ],
    "jobs_ecommerce": [
        "shopee", "lazada", "part time", "commission", "task", "like and share", 
        "high return", "investment", "agent", "grab", "tiktok"
    ],
    "tech_links": [
        "apk", "download", "link", "click", "install", "app", "otp", "system update"
    ]
}

def load_brains():
    try:
        nlp_model = spacy.load("en_core_web_sm")
    except OSError:
        print("Downloading spaCy NLP model...")
        spacy.cli.download("en_core_web_sm")
        nlp_model = spacy.load("en_core_web_sm")

    acoustic_brain = joblib.load(AUDIO_MODEL_PATH) if os.path.exists(AUDIO_MODEL_PATH) else None 
    text_pipeline = joblib.load(TEXT_MODEL_PIPELINE_PATH) if os.path.exists(TEXT_MODEL_PIPELINE_PATH) else None
    return acoustic_brain, text_pipeline, nlp_model

def extract_massive_features(file_path):
    y, sr_rate = librosa.load(file_path, duration=3, res_type='kaiser_fast')
    mfcc = librosa.feature.mfcc(y=y, sr=sr_rate, n_mfcc=60)
    mel = librosa.feature.melspectrogram(y=y, sr=sr_rate, n_mels=128)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr_rate)
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr_rate)
    y_harmonic = librosa.effects.harmonic(y)
    tonnetz = librosa.feature.tonnetz(y=y_harmonic, sr=sr_rate)

    features = []
    for audio_data in [mfcc, mel, chroma, contrast, tonnetz]:
        features.extend([
            np.mean(audio_data, axis=1), np.std(audio_data, axis=1),
            np.min(audio_data, axis=1), np.max(audio_data, axis=1)
        ])
    return np.hstack(features)

def extract_nlp_entities(text, nlp_model):
    if not nlp_model:
        return []
    doc = nlp_model(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'MONEY', 'DATE', 'TIME', 'PERSON']:
            entities.append(f"{ent.text} ({ent.label_})")
    return list(set(entities))

def calculate_malaysian_risk(text, ml_score):
    text_lower = text.lower()
    found_keywords = []
    categories_hit = set()
    urgency_flags = []

    for category, words in MALAYSIAN_SCAM_PATTERNS.items():
        for w in words:
            if w in text_lower:
                found_keywords.append(w)
                categories_hit.add(category)
                if category == "urgency_and_threats":
                    urgency_flags.append(w)

    num_categories = len(categories_hit)
    num_keywords = len(set(found_keywords))
    heuristic_score = 0.0

    # Strict alignment mapping to ensure context directly maps to high-risk scores
    if num_categories >= 3:
        heuristic_score = 95.0
    elif num_categories == 2:
        heuristic_score = 75.0
    elif num_keywords >= 3:
        heuristic_score = 55.0
    elif num_keywords >= 1:
        heuristic_score = 35.0

    final_score = max(ml_score, heuristic_score)
    return final_score, list(set(found_keywords)), list(set(urgency_flags))


# =================================================================
# FEATURE INTERFACE: AUDIO & CALL SHIELD SCANNER
# =================================================================
def analyze_audio_file(file_path):
    """Used uniformly by Call Shield and Audio Scanning portals."""
    results = {"status": "success", "transcript": "", "acoustic_features": {}, "scam_probability": 0.0, "verdict": "SAFE"}

    try:
        acoustic_model, text_pipeline, nlp_model = load_brains()

        # --- 1. ACOUSTIC ANALYSIS ---
        y, sr_rate = librosa.load(file_path, sr=16000)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr_rate)
        actual_bpm = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr_rate)[0]
        average_pitch = float(np.mean(spectral_centroids))
        
        acoustic_score = 15.0 
        used_ml = False
        
        if acoustic_model:
            try:
                ml_features = extract_massive_features(file_path)
                expected_features = getattr(acoustic_model, 'n_features_in_', len(ml_features))
                if len(ml_features) == expected_features:
                    acoustic_score = acoustic_model.predict_proba([ml_features])[0][1] * 100.0
                    used_ml = True
            except Exception:
                pass
        
        if not used_ml:
            if 110 <= actual_bpm <= 145: acoustic_score += 45.0
            if np.std(spectral_centroids) < 900.0: acoustic_score += 40.0
            
        acoustic_score = min(100.0, acoustic_score)

        # --- 2. TRANSCRIPTION (WITH GLOBAL FALLBACK) ---
        transcript = "[Transcription Unavailable]"
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
            sf.write(tmp_wav.name, y, sr_rate)
            recognizer = sr.Recognizer()
            with sr.AudioFile(tmp_wav.name) as source:
                audio_data = recognizer.record(source)
                try: 
                    # Try Malaysian English first
                    transcript = recognizer.recognize_google(audio_data, language="en-MY").lower()
                except sr.UnknownValueError:
                    try:
                        # Fallback to Malay
                        transcript = recognizer.recognize_google(audio_data, language="ms-MY").lower()
                    except sr.UnknownValueError:
                        try:
                            # NEW: Fallback to Standard/American English for robocalls
                            transcript = recognizer.recognize_google(audio_data, language="en-US").lower()
                        except sr.UnknownValueError:
                            pass
                except Exception: 
                    pass
        if os.path.exists(tmp_wav.name): os.remove(tmp_wav.name)

        # --- 3. SCORING ENGINE ---
        extracted_entities = []
        text_risk_score = 0.0
        found_red_flags = []

        if transcript != "[Transcription Unavailable]":
            extracted_entities = extract_nlp_entities(transcript, nlp_model)
            base_ml_score = 0.0
            if text_pipeline:
                try:
                    base_ml_score = text_pipeline.predict_proba([transcript])[0][1] * 100.0
                except Exception:
                    pass
            
            text_risk_score, found_red_flags, _ = calculate_malaysian_risk(transcript, base_ml_score)
            
            # --- THE MATH PENALTY OVERRIDE ---
            # If the Text AI catches blatant scam words (Score 75+), 
            # do not let a "normal" sounding acoustic score drag the average down!
            if text_risk_score >= 75.0:
                final_probability = max(text_risk_score, acoustic_score)
            else:
                final_probability = (acoustic_score * 0.4) + (text_risk_score * 0.6)
        else:
            final_probability = acoustic_score

        # --- 4. NEW STRATIFIED VERDICT LOGIC (0-20, 20-50, 50-100) ---
        if final_probability >= 50.0:
            verdict = "SCAM"
        elif final_probability >= 20.0:
            verdict = "SUSPICIOUS"
        else:
            verdict = "SAFE"

        results.update({
            "transcript": transcript,
            "scam_probability": round(final_probability, 2),
            "verdict": verdict,
            "acoustic_features": {
                "average_pitch": round(average_pitch, 2),
                "speech_rate_bpm": round(actual_bpm, 1),
                "red_flags": found_red_flags,
                "nlp_entities": extracted_entities
            }
        })
        return results

    except Exception as e:
        return {"status": "error", "error_message": str(e)}


# =================================================================
# FEATURE INTERFACE: TEXT SCANNER
# =================================================================
def analyze_text_content(text):
    """Used by the Text/SMS scanning portal."""
    _, text_pipeline, nlp_model = load_brains()
    
    extracted_entities = extract_nlp_entities(text, nlp_model)
    
    base_ml_score = 0.0
    if text_pipeline:
        try:
            base_ml_score = text_pipeline.predict_proba([text.lower()])[0][1] * 100.0
        except Exception:
            pass

    final_score, risk_keywords, urgency_flags = calculate_malaysian_risk(text, base_ml_score)

    # --- NEW STRATIFIED VERDICT LOGIC (0-20, 20-50, 50-100) ---
    if final_score >= 50.0:
        verdict = "SCAM"
    elif final_score >= 20.0:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"

    return {
        "score": round(min(100.0, final_score), 2),
        "verdict": verdict,
        "risk_keywords": risk_keywords,
        "urgency_flags": urgency_flags,
        "nlp_entities": extracted_entities 
    }