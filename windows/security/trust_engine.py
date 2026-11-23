"""
ROCXY Trust Score and Risk Assessment Engine
Initial rule-based security scoring module.
"""

def calculate_trust_score(
    voice_match: float,
    liveness: float,
    anti_replay: float,
    deepfake_confidence: float
):
    """
    Inputs must be values from 0 to 100.
    Higher deepfake_confidence means stronger evidence
    of a deepfake.
    """

    values = [
        voice_match,
        liveness,
        anti_replay,
        deepfake_confidence
    ]

    if any(not isinstance(v, (int, float)) or not 0 <= v <= 100
           for v in values):
        raise ValueError("All scores must be between 0 and 100.")

    score = (
        voice_match * 0.40
        + liveness * 0.25
        + anti_replay * 0.20
        + (100 - deepfake_confidence) * 0.15
    )

    score = round(score, 2)

    if score >= 85:
        risk = "LOW"
    elif score >= 65:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {
        "trust_score": score,
        "risk_level": risk,
        "authorization": "REQUIRES_VERIFICATION"
    }


if __name__ == "__main__":
    result = calculate_trust_score(
        voice_match=95,
        liveness=90,
        anti_replay=95,
        deepfake_confidence=5
    )

    print("ROCXY SECURITY ASSESSMENT")
    print(result)

