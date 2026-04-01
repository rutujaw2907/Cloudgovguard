def build_remediation_summary(violations):
    return [
        {
            "policy": v["policy_name"],
            "resource": v["resource_name"],
            "severity": v["severity"],
            "fix": v["remediation"]
        }
        for v in violations
    ]