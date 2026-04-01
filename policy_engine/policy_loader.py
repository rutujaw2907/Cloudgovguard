import os
import yaml
from app.config import POLICY_DIR

def load_policies():
    policies = []
    for file_name in os.listdir(POLICY_DIR):
        if file_name.endswith(".yaml") or file_name.endswith(".yml"):
            full_path = os.path.join(POLICY_DIR, file_name)
            with open(full_path, "r", encoding="utf-8") as f:
                policies.append(yaml.safe_load(f))
    return policies