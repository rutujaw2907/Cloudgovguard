import networkx as nx

def build_attack_graph(violations):
    G = nx.DiGraph()

    has_public_ssh = any(v["policy_id"] == "NET001" for v in violations)
    has_admin_policy = any(v["policy_id"] == "IAM001" for v in violations)

    if has_public_ssh:
        G.add_edge("Public SSH", "Initial Access")

    if has_admin_policy:
        G.add_edge("Excessive IAM Privileges", "Privilege Escalation")

    if has_public_ssh and has_admin_policy:
        G.add_edge("Initial Access", "Privilege Escalation")
        G.add_edge("Privilege Escalation", "Cloud Compromise")

    return list(G.edges())