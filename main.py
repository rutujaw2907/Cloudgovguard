# main.py

from cloud_adapter.oci_collector import OCICollector
from normalizer.resource_parser import normalize
from policy_engine.policy_loader import load_policies
from policy_engine.evaluator import evaluate
from risk_engine.scoring import calculate_score


def run_scan():
    print("[1] Collecting data...")
    raw_data = OCICollector().collect()

    print("[2] Normalizing...")
    normalized = normalize(raw_data)

    print("[3] Loading policies...")
    policies = load_policies()

    print("[4] Evaluating...")
    violations = evaluate(normalized, policies)

    print("[5] Calculating score...")
    score = calculate_score(violations)

    return {
        "resources": {"total": len(normalized)},
        "violations": violations,
        "score": score
    }


if __name__ == "__main__":
    result = run_scan()
    print("\nFINAL OUTPUT:\n", result)