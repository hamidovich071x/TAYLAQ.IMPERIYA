
import os
from flask import Flask, jsonify
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecret")

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    url = urlparse(DATABASE_URL)
    return psycopg2.connect(
        dbname=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            items TEXT,
            total INTEGER,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "<h1>Taylaq Food Production Server 🚀</h1>"

@app.route("/orders")
def orders():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, items, total, status, created_at FROM orders ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "items": r[1],
            "total": r[2],
            "status": r[3],
            "created_at": str(r[4])
        })
    return jsonify(data)

if DATABASE_URL:
    init_db()

if __name__ == "__main__":
    app.run()
