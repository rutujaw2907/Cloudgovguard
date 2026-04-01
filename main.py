import json

from app.config import RESOURCES_JSON
from app.db import init_db, get_connection
from cloud_adapter.oci_collector import OCICollector
from normalizer.resource_parser import normalize_all
from policy_engine.policy_loader import load_policies
from policy_engine.evaluator import evaluate_resources
from risk_engine.scoring import calculate_score
from visualization.attack_graph import build_attack_graph


def save_resources(resources):
    with open(RESOURCES_JSON, "w", encoding="utf-8") as f:
        json.dump(resources, f, indent=2)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM resources")

    for r in resources:
        cur.execute("""
            INSERT INTO resources (provider, resource_type, resource_name, raw_data)
            VALUES (?, ?, ?, ?)
        """, (
            r.get("provider"),
            r.get("resource_type"),
            r.get("resource_name"),
            json.dumps(r)
        ))

    conn.commit()
    conn.close()


def save_violations(violations):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM violations")

    for v in violations:
        cur.execute("""
            INSERT INTO violations
            (policy_id, policy_name, framework, control_id, severity,
             resource_name, resource_type, reason, remediation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            v["policy_id"],
            v["policy_name"],
            v["framework"],
            v["control_id"],
            v["severity"],
            v["resource_name"],
            v["resource_type"],
            v["reason"],
            v["remediation"]
        ))

    conn.commit()
    conn.close()


def save_score(score_data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM scores")

    cur.execute("""
        INSERT INTO scores
        (total_score, critical_count, high_count, medium_count, low_count)
        VALUES (?, ?, ?, ?, ?)
    """, (
        score_data["score"],
        score_data["critical"],
        score_data["high"],
        score_data["medium"],
        score_data["low"]
    ))

    conn.commit()
    conn.close()


def run_scan():
    print("[1] Initializing database...")
    init_db()

    print("[2] Collecting OCI resources...")
    collector = OCICollector()
    raw_data = collector.collect_all()

    print("[3] Normalizing resources...")
    resources = normalize_all(raw_data)

    print(f"[INFO] Total normalized resources: {len(resources)}")
    save_resources(resources)

    print("[4] Loading policies...")
    policies = load_policies()

    print(f"[INFO] Total policies loaded: {len(policies)}")

    print("[5] Evaluating policies...")
    violations = evaluate_resources(resources, policies)
    print(f"[INFO] Violations found: {len(violations)}")
    save_violations(violations)

    print("[6] Calculating score...")
    score_data = calculate_score(violations)
    print(f"[INFO] Security Score: {score_data['score']}")
    save_score(score_data)

    print("[7] Building attack graph...")
    edges = build_attack_graph(violations)
    print("[INFO] Attack graph edges:", edges)

    print("[DONE] Scan completed.")


if __name__ == "__main__":
    run_scan()