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

def close_db_connection(conn):
    conn.close()

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS checkboxTable(id INTEGER PRIMARY KEY, checkbox_column BOOLEAN)''')
    conn.commit()
    conn.close()

@app.route('/tasks', methods=['GET', 'POST'])
def tasks_page():
    if request.method == 'POST':
        checkbox_id = request.form.get['checkbox_id']
        checkbox_value = request.form['checkboxtable_' + checkbox_id] == 'on'
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''UPDATE checkboxTable SET checkbox_column=? WHERE id=?''', (checkbox_value, checkbox_id))
        conn.commit()
        conn.close()
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM checkboxTable''')
        checkbox_states = cursor.fetchall()
        conn.close()
    return render_template('tasks.html', checkbox_states=checkbox_states)

@app.route('/', methods=['GET', 'POST'])
def dropdown(selected_colour = None):
    colours = ['Red', 'Blue', 'Black', 'Orange']
    selected_colour = request.form.get('colour')
    return render_template('index.html', colours=colours, selected_colour=selected_colour)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

