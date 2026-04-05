from flask import Flask, jsonify
from app.db import get_connection

app = Flask(__name__)


@app.route("/api/resources")
def get_resources():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as count FROM resources")
    count = cur.fetchone()["count"]

    conn.close()

    return jsonify({
        "total_resources": count
    })


@app.route("/api/violations")
def get_violations():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM violations")
    rows = cur.fetchall()

    violations = [dict(r) for r in rows]

    conn.close()

    return jsonify(violations)


@app.route("/api/score")
def get_score():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM scores ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()

    conn.close()

    return jsonify({
        "score": row["total_score"],
        "critical": row["critical_count"],
        "high": row["high_count"],
        "medium": row["medium_count"],
        "low": row["low_count"]
    })