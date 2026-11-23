"""
ROCXY Voiceprint Recognition Engine
Experimental audio feature comparison.
"""

import wave
import numpy as np


def extract_features(audio_path):
    """Extract a basic spectral feature vector from WAV audio."""

    with wave.open(audio_path, "rb") as audio:
        if audio.getnchannels() != 1 or audio.getsampwidth() != 2:
            raise ValueError("Expected mono 16-bit WAV audio.")

        sample_rate = audio.getframerate()
        samples = np.frombuffer(
            audio.readframes(audio.getnframes()),
            dtype=np.int16
        ).astype(np.float32)

    if len(samples) < 1024:
        raise ValueError("Audio sample is too short.")

    samples /= 32768.0

    spectrum = np.abs(np.fft.rfft(samples * np.hanning(len(samples))))
    features = np.log1p(spectrum)

    return {
        "sample_rate": sample_rate,
        "features": features
    }


def compare_voice(reference_path, test_path):
    """Compare two experimental spectral feature vectors."""

    reference = extract_features(reference_path)
    test = extract_features(test_path)

    if reference["sample_rate"] != test["sample_rate"]:
        raise ValueError("Audio sample rates must match.")

    a = reference["features"]
    b = test["features"]

    size = min(len(a), len(b))
    a = a[:size]
    b = b[:size]

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        similarity = 0.0
    else:
        similarity = float(np.dot(a, b) / denominator)

    return round(similarity * 100, 2)


if __name__ == "__main__":
    print("ROCXY Voiceprint Engine initialized.")
    print("Experimental spectral comparison only.")
