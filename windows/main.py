"""
ROCXY - Windows Voice Security Framework
Integrated development prototype.
"""

import os

from security.profile_manager import ProfileManager
from security.trust_engine import calculate_trust_score
from security.voice_engine import record_voice, validate_audio
from security.anti_replay import check_replay, register_audio
from security.liveness_engine import LivenessEngine
from security.deepfake_engine import DeepfakeEngine
from security.voiceprint_engine import compare_voice


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
VOICE_DIR = os.path.join(DATA_DIR, "voices")


def banner():
    print("\n" + "=" * 48)
    print("              ROCXY v1.0")
    print("       ADVANCED VOICE SECURITY SYSTEM")
    print("=" * 48)


def profiles_menu(manager):
    print("\n--- USER PROFILES ---")
    print("1. Register profile")
    print("2. View profiles")

    choice = input("Select: ").strip()

    if choice == "1":
        name = input("Enter user name: ")
        print(manager.register_user(name))

    elif choice == "2":
        for user in manager.list_users():
            print(user["name"], "-", user["status"])


def record_test_audio():
    os.makedirs(VOICE_DIR, exist_ok=True)
    path = os.path.join(VOICE_DIR, "test_voice.wav")

    record_voice(path)

    if validate_audio(path):
        print("Audio validation successful.")
        return path

    print("Audio validation failed.")
    return None


def audio_security_menu():
    print("\n--- AUDIO SECURITY ---")
    path = os.path.join(VOICE_DIR, "test_voice.wav")

    if not os.path.isfile(path):
        print("Record an audio sample first.")
        return

    print("1. Check exact replay")
    print("2. Register audio fingerprint")
    print("3. Check deepfake engine status")

    choice = input("Select: ").strip()

    if choice == "1":
        print(check_replay(path))

    elif choice == "2":
        register_audio(path)
        print("Audio fingerprint registered.")

    elif choice == "3":
        detector = DeepfakeEngine()
        print(detector.analyze_audio(path))


def trust_demo():
    print("\n--- TRUST SCORE DEMONSTRATION ---")
    print("This is demonstration input, not measured security evidence.")

    try:
        voice = float(input("Voice match score (0-100): "))
        live = float(input("Liveness score (0-100): "))
        replay = float(input("Anti-replay score (0-100): "))
        deepfake = float(input("Deepfake confidence (0-100): "))

        print(calculate_trust_score(
            voice, live, replay, deepfake
        ))

    except ValueError as error:
        print("Invalid input:", error)


def main():
    os.makedirs(VOICE_DIR, exist_ok=True)

    manager = ProfileManager()
    liveness = LivenessEngine()

    while True:
        banner()

        print("1. User Profile Management")
        print("2. Record Voice Sample")
        print("3. Audio Security")
        print("4. Generate Liveness Challenge")
        print("5. Trust Score Demonstration")
        print("6. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            profiles_menu(manager)

        elif choice == "2":
            record_test_audio()

        elif choice == "3":
            audio_security_menu()

        elif choice == "4":
            print("\nSpeak this challenge:")
            print(liveness.generate_challenge())
            print("Challenge expires after 30 seconds.")
            print("Speech recognition integration is pending.")

        elif choice == "5":
            trust_demo()

        elif choice == "6":
            print("ROCXY shutting down.")
            break

        else:
            print("Invalid option.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
