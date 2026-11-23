"""
ROCXY - Windows Voice Security Framework
Main application entry point.
"""

import os
import json
from datetime import datetime

APP_NAME = "ROCXY"
VERSION = "1.0.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROFILE_FILE = os.path.join(DATA_DIR, "profiles.json")


def initialize():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)


def load_profiles():
    with open(PROFILE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def register_profile():
    profiles = load_profiles()

    if len(profiles) >= 5:
        print("Maximum of 5 profiles reached.")
        return

    name = input("Enter profile name: ").strip()

    if not name:
        print("Profile name cannot be empty.")
        return

    profiles.append({
        "id": len(profiles) + 1,
        "name": name,
        "created_at": datetime.now().isoformat(),
        "status": "registered"
    })

    with open(PROFILE_FILE, "w", encoding="utf-8") as file:
        json.dump(profiles, file, indent=4)

    print(f"Profile created: {name}")


def show_profiles():
    profiles = load_profiles()

    if not profiles:
        print("No profiles registered.")
        return

    print("\nROCXY PROFILES")
    for profile in profiles:
        print(f"{profile['id']}. {profile['name']} - {profile['status']}")


def main():
    initialize()

    while True:
        print("\n" + "=" * 40)
        print(f"       {APP_NAME} v{VERSION}")
        print(" Advanced Voice Security Framework")
        print("=" * 40)
        print("1. Register Profile")
        print("2. View Profiles")
        print("3. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            register_profile()
        elif choice == "2":
            show_profiles()
        elif choice == "3":
            print("ROCXY shutting down.")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
