def normalize_users(users):
    normalized = []
    for user in users:
        normalized.append({
            "provider": "oracle",
            "resource_type": "iam_user",
            "resource_name": user.name,
            "mfa_enabled": None,
            "description": getattr(user, "description", "")
        })
    return normalized


def normalize_policies(policies):
    normalized = []
    for policy in policies:
        statements = getattr(policy, "statements", [])
        normalized.append({
            "provider": "oracle",
            "resource_type": "iam_policy",
            "resource_name": policy.name,
            "statements": statements
        })
    return normalized


def normalize_security_lists(security_lists):
    normalized = []
    for sec_list in security_lists:
        ingress_rules = getattr(sec_list, "ingress_security_rules", [])
        for rule in ingress_rules:
            source = getattr(rule, "source", None)
            protocol = getattr(rule, "protocol", None)

            port_min = None
            port_max = None

            if getattr(rule, "tcp_options", None):
                port_min = getattr(rule.tcp_options, "destination_port_range", None).min \
                    if getattr(rule.tcp_options, "destination_port_range", None) else None
                port_max = getattr(rule.tcp_options, "destination_port_range", None).max \
                    if getattr(rule.tcp_options, "destination_port_range", None) else None

            normalized.append({
                "provider": "oracle",
                "resource_type": "security_rule",
                "resource_name": sec_list.display_name,
                "source": source,
                "protocol": protocol,
                "port": port_min,
                "port_range_max": port_max
            })
    return normalized


def normalize_buckets(buckets):
    normalized = []
    for bucket in buckets:
        normalized.append({
            "provider": "oracle",
            "resource_type": "bucket",
            "resource_name": bucket.name,
            "public_access_type": getattr(bucket, "public_access_type", "Unknown"),
            "kms_key_id": getattr(bucket, "kms_key_id", None)
        })
    return normalized


def normalize_all(raw):
    resources = []
    resources.extend(normalize_users(raw.get("users", [])))
    resources.extend(normalize_policies(raw.get("policies", [])))
    resources.extend(normalize_security_lists(raw.get("security_lists", [])))
    resources.extend(normalize_buckets(raw.get("buckets", [])))
    return resources