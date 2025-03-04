from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "biba.db"

# Функція для ініціалізації бази даних
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY, 
                        balance INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

init_db()  # Ініціалізуємо базу при запуску

@app.route("/")
def index():
    return render_template("index.html")

# Отримати баланс користувача
@app.route("/get_balance", methods=["POST"])
def get_balance():
    data = request.json
    user_id = data.get("user_id")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result is None:
        cursor.execute("INSERT INTO users (user_id, balance) VALUES (?, ?)", (user_id, 0))
        conn.commit()
        balance = 0
    else:
        balance = result[0]

    conn.close()
    return jsonify({"balance": balance})

# Додавання монет при кліку
@app.route("/tap", methods=["POST"])
def tap():
    data = request.json
    user_id = data.get("user_id")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result is None:
        balance = 1
        cursor.execute("INSERT INTO users (user_id, balance) VALUES (?, ?)", (user_id, balance))
    else:
        balance = result[0] + 1
        cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance, user_id))

    conn.commit()
    conn.close()
    return jsonify({"balance": balance})

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0', port=9462, use_reloader=False)
