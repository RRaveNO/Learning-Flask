from flask import Flask, render_template, url_for, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

def close_db_connection():
    conn=get_db_connection()
    if conn is not None:
        conn.close()

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS checkboxes(id INTEGER PRIMARY KEY, checkbox_column TEXT NOT NULL)''')
    conn.commit()
    close_db_connection()

@app.route('/tasks', methods = ['GET', 'POST'])
def tasks_page():
    if request.method == 'GET':
        checkbox_value = request.args.get('checkbox')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO checkboxes(checkbox_column) VALUES (checkbox_column)", (checkbox_value,))
        cursor.execute('''SELECT FROM checkboxes''')
        checkboxes = cursor.fetchall()
        conn.commit()
        close_db_connection()
    return render_template('tasks.html', checkboxes=checkboxes)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

