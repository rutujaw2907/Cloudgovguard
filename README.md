# 🚀 CloudGovGuard

### Multi-Cloud Governance & Security Posture Analyzer

---

## 📌 Overview

**CloudGovGuard** is a Cloud Security Posture Management (CSPM) tool that analyzes cloud infrastructure, detects security misconfigurations, enforces governance policies, and provides compliance insights.

The system is inspired by enterprise tools like Wiz and Orca Security, and is designed to be **multi-cloud ready** with initial integration for **Oracle Cloud Infrastructure (OCI)**.

---

## 🎯 Problem Statement

Cloud providers offer infrastructure and access control, but they **do not enforce security best practices**.

Organizations face risks like:

* Publicly exposed resources
* Weak IAM configurations
* Lack of compliance visibility
* Manual security audits

---

## 💡 Solution

CloudGovGuard solves this by:

* Collecting cloud configuration data
* Applying **policy-as-code governance rules**
* Detecting violations automatically
* Mapping issues to compliance frameworks
* Generating a security score
* Providing remediation guidance
* Visualizing everything in a dashboard

---

## 🏗️ System Architecture

```
Cloud Infrastructure (OCI)
          ↓
   OCI Data Collector
          ↓
   Resource Normalizer
          ↓
   Policy Engine (YAML)
          ↓
   Violation Detector
          ↓
   Risk Scoring Engine
          ↓
   Remediation Advisor
          ↓
   Dashboard (Flask UI)
```

---

## ⚙️ Tech Stack

| Component     | Technology     |
| ------------- | -------------- |
| Backend       | Python (Flask) |
| Cloud API     | OCI SDK        |
| Data Handling | Pandas         |
| Policies      | YAML           |
| Visualization | Chart.js       |
| Graph Engine  | NetworkX       |
| Database      | SQLite         |

---

## 📁 Project Structure

```
cloudgovguard/

cloud_adapter/
   oci_collector.py

normalizer/
   resource_parser.py

policy_engine/
   policy_loader.py
   evaluator.py

policies/
   block_public_ssh.yaml
   mfa_required.yaml

risk_engine/
   scoring.py

database/
   db.py

app.py
main.py
```

---

## 🔍 Key Features

### 🔹 1. Cloud Data Collection

* Fetches IAM, network, and resource configurations from OCI

---

### 🔹 2. Resource Normalization

* Converts cloud-specific data into a unified format
* Enables multi-cloud support (AWS, Azure)

---

### 🔹 3. Policy-as-Code Engine

* Policies defined in YAML
* No code changes required to add rules

Example:

```yaml
name: Block Public SSH
resource: security_rule
condition:
  port: 22
  source: 0.0.0.0/0
```

---

### 🔹 4. Violation Detection

* Matches resources against policies
* Generates security violations

---

### 🔹 5. Risk Scoring

* Calculates overall cloud security score

Formula:

```
score = 100 - (critical*10 + high*5 + medium*2)
```

---

### 🔹 6. Compliance Mapping

* Maps policies to frameworks like CIS

Example:

| Policy           | Framework | Control |
| ---------------- | --------- | ------- |
| Block Public SSH | CIS       | CIS 4.1 |

---

### 🔹 7. Remediation Guidance

* Suggests fixes for each violation

---

### 🔹 8. Interactive Dashboard

* Displays:

  * Total resources
  * Violations
  * Security score
  * Severity charts

---

## 🧪 Demo Scenarios

### ✅ Scenario 1: Add Policy

* Add new YAML policy
* Run scan
* New violation appears

---

### ✅ Scenario 2: Remove Policy

* Delete policy
* Run scan
* Violation disappears

---

### ✅ Scenario 3: Fix Cloud Issue

* Modify OCI configuration
* Run scan
* Score improves

---

## ▶️ How to Run

### 1. Install dependencies

```
pip install flask pyyaml oci
```

---

### 2. Run scan

```
python main.py
```

---

### 3. Start dashboard

```
python app.py
```

---

### 4. Open browser

```
http://127.0.0.1:5000
```

---

## 🔐 OCI Setup

1. Configure OCI CLI:

```
~/.oci/config
```

2. Add credentials:

* Tenancy OCID
* User OCID
* Key file

---

## 🚀 Future Enhancements

* Multi-cloud support (AWS, Azure)
* Automated remediation engine
* Attack path visualization
* Real-time monitoring
* Integration with SIEM tools

---

## 📈 Use Cases

* Cloud security auditing
* Governance enforcement
* Compliance reporting
* Risk analysis

---

## 🧠 Key Insight

CloudGovGuard demonstrates that:

> Cloud providers secure infrastructure,
> but governance must be enforced externally.

---

## 👥 Team Roles

### Cloud Security Engineer

* OCI integration
* Data collection
* Normalization

### Governance Engineer

* Policy design
* Risk scoring
* Compliance mapping

---

## 🏁 Conclusion

CloudGovGuard provides a scalable and flexible way to enforce cloud governance using **policy-as-code**, making it suitable for modern cloud security challenges.

---

## ⭐ Resume Highlight

Built a multi-cloud security posture management tool that detects IAM, network, and storage misconfigurations using policy-as-code and provides compliance insights aligned with CIS benchmarks.
