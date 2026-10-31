import os, time
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "apppass"),
        database=os.getenv("DB_NAME", "notesdb"),
    )

def init_db():
    for _ in range(30):
        try:
            c = get_conn()
            cur = c.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS notes (id INT AUTO_INCREMENT PRIMARY KEY, text VARCHAR(255))")
            c.commit(); c.close()
            return
        except Exception:
            time.sleep(2)

@app.route("/")
def list_notes():
    c = get_conn(); cur = c.cursor()
    cur.execute("SELECT id, text FROM notes")
    rows = cur.fetchall(); c.close()
    return jsonify(notes=[{"id": r[0], "text": r[1]} for r in rows])

@app.route("/add", methods=["GET", "POST"])
def add_note():
    text = request.values.get("text", "hello")
    c = get_conn(); cur = c.cursor()
    cur.execute("INSERT INTO notes (text) VALUES (%s)", (text,))
    c.commit(); c.close()
    return jsonify(status="added", text=text)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
