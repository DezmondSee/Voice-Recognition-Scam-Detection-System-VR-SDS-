import librosa
import numpy as np

def extract_features(file_path):
    try:
        audio, sr = librosa.load(file_path, res_type='kaiser_fast', duration=3.0)
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
        return np.mean(mfccs.T, axis=0).reshape(1, -1)
    except:
        return None