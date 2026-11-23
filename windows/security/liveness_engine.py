"""
ROCXY Liveness Detection Engine
Random challenge-response verification.
"""

import secrets
import time

CHALLENGES = [
    "ROCXY secure access",
    "My voice is my identity",
    "Verify my voice now",
    "Security comes first",
    "ROCXY authentication"
]

class LivenessEngine:

    def __init__(self):
        self.challenge = None
        self.created_at = None

    def generate_challenge(self):
        self.challenge = secrets.choice(CHALLENGES)
        self.created_at = time.time()

        return self.challenge

    def verify_response(self, recognized_text):
        if self.challenge is None:
            return {
                "verified": False,
                "message": "No active challenge."
            }

        if time.time() - self.created_at > 30:
            self.challenge = None
            return {
                "verified": False,
                "message": "Challenge expired."
            }

        expected = self.challenge.lower().strip()
        received = recognized_text.lower().strip()

        verified = received == expected

        self.challenge = None

        return {
            "verified": verified,
            "message": (
                "Challenge response matched."
                if verified
                else "Challenge response failed."
            )
        }


if __name__ == "__main__":
    engine = LivenessEngine()

    challenge = engine.generate_challenge()

    print("\nROCXY LIVE VOICE CHALLENGE")
    print("Speak this phrase:")
    print(challenge)

    response = input("\nEnter recognized speech: ")

    print(engine.verify_response(response))
