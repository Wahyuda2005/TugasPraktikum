from flask import Flask, render_template_string, request
import sqlite3

app = Flask(__name__)

# Fungsi inisialisasi database SQLite
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    init_db()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        msg = request.form.get('message')
        if msg:
            cursor.execute("INSERT INTO messages (content) VALUES (?)", (msg,))
            conn.commit()
            
    cursor.execute("SELECT content FROM messages")
    messages = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return render_template_string('''
        <h2>Aplikasi Python Flask + SQLite + Docker + Jenkins</h2>
        <form method="POST">
            <input type="text" name="message" placeholder="Tulis pesan ke database..." required>
            <button type="submit">Simpan</button>
        </form>
        <h3>Daftar Pesan dari Database:</h3>
        <ul>
            {% for m in messages %}
                <li>{{ m }}</li>
            {% endfor %}
        </ul>
    ''', messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
