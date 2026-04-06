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


def evaluate_policy(normalized, policies):
    violations = []

    for resource in normalized:
        for policy in policies:
            # add your checking logic here
            pass

    return violations