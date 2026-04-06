from app.db import get_connection, init_db

init_db()

conn = get_connection()
cur = conn.cursor()

cur.execute("DELETE FROM resources")
cur.execute("DELETE FROM violations")
cur.execute("DELETE FROM scores")

resources = [
    ("compute_instance", "VM-1", '{"ip":"129.1.1.1"}'),
    ("bucket", "Bucket-1", '{"public":true}'),
    ("iam_user", "User-1", '{"mfa":false}'),
    ("security_rule", "SSH Rule", '{"port":22,"source":"0.0.0.0/0"}')
]

cur.executemany("""
    INSERT INTO resources (resource_type, resource_name, metadata)
    VALUES (?, ?, ?)
""", resources)

violations = [
    ("Block Public SSH", "SSH Rule", "CRITICAL", "Port 22 is open to 0.0.0.0/0", "Restrict SSH access to trusted IP ranges"),
    ("MFA Required", "User-1", "HIGH", "MFA is not enabled for this IAM user", "Enable MFA for all IAM users"),
    ("Bucket Must Not Be Public", "Bucket-1", "HIGH", "Bucket is publicly accessible", "Disable public access on the bucket")
]

cur.executemany("""
    INSERT INTO violations (policy_name, resource_name, severity, reason, remediation)
    VALUES (?, ?, ?, ?, ?)
""", violations)

cur.execute("""
    INSERT INTO scores (total_score, critical_count, high_count, medium_count, low_count)
    VALUES (?, ?, ?, ?, ?)
""", (74, 1, 2, 0, 0))

conn.commit()
conn.close()

print("Seed data inserted successfully.")