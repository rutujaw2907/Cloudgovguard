def normalize_users(users):
    result = []

    for user in users:
        result.append({
            "provider": "oracle",
            "resource_type": "iam_user",
            "resource_name": user.name,
            "mfa_enabled": False  # OCI limitation (keep for policy engine)
        })

    return result


def normalize_policies(policies):
    result = []

    for policy in policies:
        result.append({
            "provider": "oracle",
            "resource_type": "iam_policy",
            "resource_name": policy.name,
            "statements": policy.statements
        })

    return result


def normalize_security_lists(security_lists):
    result = []

    for sec in security_lists:
        rules = sec.ingress_security_rules or []

        for rule in rules:
            port = None

            if rule.tcp_options and rule.tcp_options.destination_port_range:
                port = rule.tcp_options.destination_port_range.min

            result.append({
                "provider": "oracle",
                "resource_type": "security_rule",
                "resource_name": sec.display_name,
                "source": rule.source,
                "protocol": rule.protocol,
                "port": port
            })

    return result


def normalize_buckets(buckets):
    result = []

    for bucket in buckets:
        result.append({
            "provider": "oracle",
            "resource_type": "bucket",
            "resource_name": bucket.name,
            "public_access": bucket.public_access_type,
            "encrypted": bucket.kms_key_id is not None
        })

    return result


def normalize_all(raw):
    resources = []

    resources += normalize_users(raw.get("users", []))
    resources += normalize_policies(raw.get("policies", []))
    resources += normalize_security_lists(raw.get("security_lists", []))
    resources += normalize_buckets(raw.get("buckets", []))

    return resources