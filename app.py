from flask import Flask, jsonify, render_template
import random

app = Flask(__name__, static_folder="static", template_folder="templates")

# Mock database for demonstration
# In a real app, this would come from AWS/Azure/GCP APIs
mock_db = {
    "violations": [
        {
            "id": 1,
            "policy_name": "Public SSH Access",
            "resource_name": "VM-Production-01",
            "severity": "CRITICAL",
            "reason": "Security group allows 0.0.0.0/0 on Port 22",
            "remediation": "Restrict SSH access to specific corporate CIDR blocks."
        },
        {
            "id": 2,
            "policy_name": "S3 Bucket Publicly Readable",
            "resource_name": "customer-pii-logs",
            "severity": "CRITICAL",
            "reason": "Bucket ACL set to PublicRead",
            "remediation": "Enable 'Block Public Access' at the account level."
        },
        {
            "id": 3,
            "policy_name": "MFA Not Enabled",
            "resource_name": "iam-user-admin",
            "severity": "HIGH",
            "reason": "Console access active without Multi-Factor Auth",
            "remediation": "Enforce MFA via IAM policy for all privileged users."
        }
    ],
    "compliance": [
        {"framework": "CIS Benchmark", "score": 88, "status": "Passing"},
        {"framework": "NIST 800-53", "score": 72, "status": "At Risk"},
        {"framework": "SOC2 Type II", "score": 95, "status": "Passing"},
        {"framework": "HIPAA", "score": 64, "status": "Failing"}
    ]
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/dashboard")
def dashboard():
    """
    Returns the core executive summary data.
    """
    # Calculate score based on violation counts (simulated logic)
    crit_count = len([v for v in mock_db["violations"] if v["severity"] == "CRITICAL"])
    high_count = len([v for v in mock_db["violations"] if v["severity"] == "HIGH"])
    
    return jsonify({
        "resources": {"total": 125},
        "violations": mock_db["violations"],
        "score": {
            "score": 74,
            "critical": crit_count,
            "high": high_count,
            "medium": 8,
            "low": 15
        },
        "compliance_summary": mock_db["compliance"]
    })

# Add a route for Remediation actions (Simulation)
@app.route("/api/remediate/<int:violation_id>", methods=["POST"])
def remediate(violation_id):
    """
    Simulates fixing a resource.
    """
    global mock_db
    # Remove the violation from our 'db' to simulate a fix
    mock_db["violations"] = [v for v in mock_db["violations"] if v["id"] != violation_id]
    return jsonify({"status": "success", "message": f"Remediation triggered for ID {violation_id}"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)