from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("shop.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM categories")
    categories = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(categories)

@app.route('/api/user/<tg_id>', methods=['GET'])
def get_user(tg_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify(dict(user))
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)