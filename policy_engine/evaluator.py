def resource_matches_policy(resource, policy):
    if resource.get("resource_type") != policy.get("resource"):
        return False

    condition = policy.get("condition", {})

    for key, expected_value in condition.items():
        if key == "statement_contains":
            statements = resource.get("statements", [])
            if not any(expected_value.lower() in stmt.lower() for stmt in statements):
                return False
        else:
            actual_value = resource.get(key)
            if actual_value != expected_value:
                return False

    return True


def evaluate_resources(resources, policies):
    violations = []

    for resource in resources:
        for policy in policies:
            if resource_matches_policy(resource, policy):
                violations.append({
                    "policy_id": policy["policy_id"],
                    "policy_name": policy["name"],
                    "framework": policy["framework"],
                    "control_id": policy["control_id"],
                    "severity": policy["severity"],
                    "resource_name": resource.get("resource_name"),
                    "resource_type": resource.get("resource_type"),
                    "reason": f"Resource matched condition: {policy.get('condition')}",
                    "remediation": policy["remediation"]
                })

    return violations