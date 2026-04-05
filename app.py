from flask import Flask, jsonify
from app.db import get_connection

app = Flask(__name__)

# ---------------- RESOURCES ----------------
@app.route("/api/resources")
def get_resources():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as count FROM resources")
    row = cur.fetchone()

    conn.close()

    return jsonify({
        "total_resources": row["count"] if row else 0
    })

# ---------------- VIOLATIONS ----------------
@app.route("/api/violations")
def get_violations():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM violations")
    rows = cur.fetchall()

    conn.close()

    return jsonify([dict(r) for r in rows] if rows else [])

# ---------------- SCORE ----------------
@app.route("/api/score")
def get_score():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM scores ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()

    conn.close()

    if not row:
        return jsonify({
            "score": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        })

    return jsonify({
        "score": row["total_score"],
        "critical": row["critical_count"],
        "high": row["high_count"],
        "medium": row["medium_count"],
        "low": row["low_count"]
    })

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)