import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from flask import Flask, render_template
from app.db import get_connection


app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as count FROM resources")
    resource_count = cur.fetchone()["count"]

    cur.execute("SELECT COUNT(*) as count FROM violations")
    violation_count = cur.fetchone()["count"]

    cur.execute("SELECT * FROM scores ORDER BY id DESC LIMIT 1")
    score_row = cur.fetchone()

    cur.execute("""
        SELECT severity, COUNT(*) as count
        FROM violations
        GROUP BY severity
    """)
    severity_data = cur.fetchall()

    cur.execute("""
        SELECT policy_name, COUNT(*) as count
        FROM violations
        GROUP BY policy_name
    """)
    policy_data = cur.fetchall()

    cur.execute("SELECT * FROM violations")
    violations = cur.fetchall()

    conn.close()

    score = score_row["total_score"] if score_row else 100
    critical = score_row["critical_count"] if score_row else 0
    high = score_row["high_count"] if score_row else 0
    medium = score_row["medium_count"] if score_row else 0
    low = score_row["low_count"] if score_row else 0

    return render_template(
        "index.html",
        resource_count=resource_count,
        violation_count=violation_count,
        score=score,
        critical=critical,
        high=high,
        medium=medium,
        low=low,
        severity_data=severity_data,
        policy_data=policy_data,
        violations=violations
    )


if __name__ == "__main__":
    app.run(debug=True)