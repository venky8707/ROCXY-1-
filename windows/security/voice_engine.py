"""
ROCXY Voice Engine
Initial audio capture and voice-profile processing.
"""

import wave
import os
import sounddevice as sd
import numpy as np


SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 5


def record_voice(output_path):
    """Record a five-second voice sample."""

    print("Recording started. Speak now...")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16"
    )

    sd.wait()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with wave.open(output_path, "wb") as file:
        file.setnchannels(CHANNELS)
        file.setsampwidth(2)
        file.setframerate(SAMPLE_RATE)
        file.writeframes(audio.tobytes())

    print(f"Voice sample saved: {output_path}")


def validate_audio(path):
    """Check whether an audio sample is readable."""

    if not os.path.isfile(path):
        return False

    try:
        with wave.open(path, "rb") as file:
            return (
                file.getnchannels() == 1
                and file.getframerate() == SAMPLE_RATE
                and file.getsampwidth() == 2
                and file.getnframes() > 0
            )
    except (wave.Error, OSError):
        return False


if __name__ == "__main__":
    destination = "data/test_voice.wav"
    record_voice(destination)

    if validate_audio(destination):
        print("Audio recording validated.")
    else:
        print("Audio validation failed.")
