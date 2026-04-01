import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "cloudgovguard.db")
RESOURCES_JSON = os.path.join(BASE_DIR, "data", "resources.json")
POLICY_DIR = os.path.join(BASE_DIR, "policies")