import numpy as np
import librosa
import sounddevice as sd
import threading
from controllers import scan_controller

class RealTimeScamDetector:
    def __init__(self, sample_rate=22050, duration=3):
        self.sample_rate = sample_rate
        self.duration = duration
        self.is_running = False
        self.thread = None

    def extract_features(self, audio_data):
        # Extract MFCCs for the AI model analysis
        mfccs = librosa.feature.mfcc(y=audio_data, sr=self.sample_rate, n_mfcc=40)
        return np.mean(mfccs.T, axis=0)

    def _detection_loop(self, callback):
        while self.is_running:
            # Captures 3-second audio segments from the microphone
            recording = sd.rec(int(self.duration * self.sample_rate), 
                               samplerate=self.sample_rate, channels=1)
            sd.wait()
            
            audio_segment = recording.flatten()
            features = self.extract_features(audio_segment)
            
            # Use scan_controller to get verdict and confidence
            # Ensure predict_scam is defined in your scan_controller
            prediction, confidence = scan_controller.predict_scam(features)
            callback(prediction, confidence)

    def start(self, callback):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._detection_loop, args=(callback,), daemon=True)
            self.thread.start()

    def stop(self):
        self.is_running = False