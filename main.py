from cloud_adapter.oci_collector import OCICollector
from normalizer.resource_parser import normalize
from policy_engine.policy_loader import load_policies
from policy_engine.evaluator import evaluate
from risk_engine.scoring import calculate_score

def run_scan():
    collector = OCICollector()

    raw_data = collector.collect()

    normalized = normalize(raw_data)

    policies = load_policies()

    violations = evaluate(normalized, policies)

    score = calculate_score(violations)

    return {
        "resources": {"total": len(normalized)},
        "violations": violations,
        "score": score
    }