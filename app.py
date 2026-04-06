from flask import Flask, jsonify, render_template
from app.db import get_connection

app = Flask(__name__)


# ---------------- FRONTEND ROUTE ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- API: RESOURCES ----------------
@app.route("/api/resources")
def get_resources():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) as count FROM resources")
        row = cur.fetchone()

        conn.close()

        return jsonify({
            "total_resources": row["count"] if row else 0
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- API: VIOLATIONS ----------------
@app.route("/api/violations")
def get_violations():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM violations")
        rows = cur.fetchall()

        conn.close()

        return jsonify([dict(r) for r in rows] if rows else [])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- API: SCORE ----------------
@app.route("/api/score")
def get_score():
    try:
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

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- HEALTH CHECK (DEBUGGING) ----------------
@app.route("/api/health")
def health():
    return jsonify({"status": "OK"})


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)