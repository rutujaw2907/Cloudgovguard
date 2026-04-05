import networkx as nx


def build_attack_graph(violations):
    G = nx.DiGraph()

    has_ssh = any(v["policy_id"] == "NET001" for v in violations)
    has_admin = any(v["policy_id"] == "IAM001" for v in violations)
    has_public_bucket = any(v["policy_id"] == "STO001" for v in violations)

    if has_ssh:
        G.add_edge("Internet", "VM Access")

    if has_admin:
        G.add_edge("VM Access", "Privilege Escalation")

    if has_public_bucket:
        G.add_edge("Public Bucket", "Data Exposure")

    if has_ssh and has_admin:
        G.add_edge("Privilege Escalation", "Cloud Takeover")

    return list(G.edges())