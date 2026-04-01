def calculate_score(violations):
    critical = sum(1 for v in violations if v["severity"] == "CRITICAL")
    high = sum(1 for v in violations if v["severity"] == "HIGH")
    medium = sum(1 for v in violations if v["severity"] == "MEDIUM")
    low = sum(1 for v in violations if v["severity"] == "LOW")

    score = 100 - (critical * 10 + high * 5 + medium * 2 + low * 1)
    if score < 0:
        score = 0

    return {
        "score": score,
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low
    }