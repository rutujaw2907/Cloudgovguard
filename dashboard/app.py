from flask import Flask, jsonify, render_template
from flask_cors import CORS

# IMPORTANT: templates folder is used here
app = Flask(__name__, template_folder="templates")
CORS(app)


# ======================
# MOCK DATA (temporary)
# ======================

violations = [
    {
        "id": "v1",
        "policy_name": "S3 Bucket Public Access",
        "resource_name": "prod-customer-data",
        "severity": "critical",
        "service": "S3",
        "region": "us-east-1",
        "detected_at": "2026-04-05T08:23:00Z",
        "reason": "Public access enabled",
        "remediation": "Disable public access"
    },
    {
        "id": "v2",
        "policy_name": "EC2 SSH Open",
        "resource_name": "i-123456",
        "severity": "high",
        "service": "EC2",
        "region": "us-west-2",
        "detected_at": "2026-04-05T06:15:00Z",
        "reason": "Port 22 open",
        "remediation": "Restrict SSH"
    }
]

assets = [
    {
        "id": "a1",
        "name": "prod-server",
        "type": "EC2 Instance",
        "region": "us-east-1",
        "status": "non-compliant",
        "risk_score": 85
    },
    {
        "id": "a2",
        "name": "data-bucket",
        "type": "S3 Bucket",
        "region": "us-east-1",
        "status": "compliant",
        "risk_score": 20
    }
]

frameworks = [
    {"name": "CIS", "short": "CIS", "passed": 40, "failed": 10, "total": 50},
    {"name": "NIST", "short": "NIST", "passed": 150, "failed": 30, "total": 180}
]


# ======================
# ROUTES
# ======================

# Main UI
@app.route("/")
def home():
    return render_template("index.html")


# API: Violations
@app.route("/api/violations")
def get_violations():
    return jsonify(violations)


# API: Assets
@app.route("/api/assets")
def get_assets():
    return jsonify(assets)


# API: Frameworks
@app.route("/api/frameworks")
def get_frameworks():
    return jsonify(frameworks)


# API: Dashboard summary
@app.route("/api/dashboard")
def get_dashboard():
    return jsonify({
        "total_assets": len(assets),
        "critical_risks": len([v for v in violations if v["severity"] == "critical"]),
        "violations": len(violations),
        "security_score": 75
    })


# Avoid favicon error
@app.route('/favicon.ico')
def favicon():
    return '', 204


# ======================
# RUN APP
# ======================

if __name__ == "__main__":
    app.run(debug=True)