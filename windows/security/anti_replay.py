"""
ROCXY Anti-Replay Engine
Detects exact previously registered audio files.
"""

import hashlib
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DATABASE = os.path.join(DATA_DIR, "audio_fingerprints.json")


def initialize():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(DATABASE):
        with open(DATABASE, "w", encoding="utf-8") as file:
            json.dump([], file)


def fingerprint(audio_path):
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(audio_path)

    digest = hashlib.sha256()

    with open(audio_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            digest.update(chunk)

    return digest.hexdigest()


def check_replay(audio_path):
    initialize()

    audio_hash = fingerprint(audio_path)

    with open(DATABASE, "r", encoding="utf-8") as file:
        known_hashes = json.load(file)

    if audio_hash in known_hashes:
        return {
            "replay_detected": True,
            "message": "Previously registered audio detected."
        }

    return {
        "replay_detected": False,
        "message": "No exact audio match found."
    }


def register_audio(audio_path):
    initialize()

    audio_hash = fingerprint(audio_path)

    with open(DATABASE, "r", encoding="utf-8") as file:
        known_hashes = json.load(file)

    if audio_hash not in known_hashes:
        known_hashes.append(audio_hash)

    with open(DATABASE, "w", encoding="utf-8") as file:
        json.dump(known_hashes, file, indent=4)


if __name__ == "__main__":
    print("ROCXY Anti-Replay Engine ready.")
