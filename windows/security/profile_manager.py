"""
ROCXY Profile Manager
Manages up to five registered user profiles.
"""

import json
import os
import uuid
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
PROFILE_FILE = os.path.join(DATA_DIR, "profiles.json")

MAX_PROFILES = 5


class ProfileManager:

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)

        if not os.path.exists(PROFILE_FILE):
            self.save_profiles([])

    def load_profiles(self):
        with open(PROFILE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_profiles(self, profiles):
        with open(PROFILE_FILE, "w", encoding="utf-8") as file:
            json.dump(profiles, file, indent=4)

    def register_user(self, name):
        name = name.strip()

        if not name:
            return {"success": False, "message": "Name required."}

        profiles = self.load_profiles()

        if len(profiles) >= MAX_PROFILES:
            return {"success": False, "message": "Maximum 5 profiles reached."}

        if any(p["name"].casefold() == name.casefold()
               for p in profiles):
            return {"success": False, "message": "Profile already exists."}

        profile = {
            "id": str(uuid.uuid4()),
            "name": name,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "pending_voice_enrollment"
        }

        profiles.append(profile)
        self.save_profiles(profiles)

        return {
            "success": True,
            "message": "Profile created successfully.",
            "profile": profile
        }

    def list_users(self):
        return self.load_profiles()

    def delete_user(self, profile_id):
        profiles = self.load_profiles()

        updated = [
            p for p in profiles
            if p["id"] != profile_id
        ]

        if len(updated) == len(profiles):
            return False

        self.save_profiles(updated)
        return True


if __name__ == "__main__":

    manager = ProfileManager()

    print("\nROCXY USER PROFILE MANAGER")
    print("1. Register user")
    print("2. View users")

    choice = input("Select option: ").strip()

    if choice == "1":
        name = input("Enter user name: ")
        print(manager.register_user(name))

    elif choice == "2":
        for user in manager.list_users():
            print(user["name"], user["status"])
