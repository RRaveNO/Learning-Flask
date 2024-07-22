from flask import Flask, render_template, url_for, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'tribnribnien3iu43bnu3ib53u'
check_list = ['Отменено', 'В работе', 'Завершено']


@app.route('/', methods=['GET', 'POST'])
def index():
    username = session.get('username')
    user_id = login_window(username)
    return render_template('index.html', user_id=user_id, username=username)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/tasks', methods=['GET', 'POST'])
def tasks_page():
    if request.method == 'POST':
        selected_value = request.form('option')
        request.content_length = 30
        return selected_value[1]
    else:
        return render_template('tasks.html', options=check_list)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        if password != password_confirm:
            return render_template('reg.html', error="Пароли не совпадают")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        if user:
            return render_template('reg.html', error="Пользователь уже существует")
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            db.commit()
            return redirect(url_for('login'))
    return render_template('reg.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE username=?''', (username,))
        user = cursor.fetchone()
        if user:
            if check_password_hash(user[2], password):
                session['username'] = username
                return redirect(url_for('index'))
            else:
                error = "Неправильный пароль"
        else:
            error = "Неправильное имя пользователя"
        return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect((url_for('login')))

def db_connection():
    conn = sqlite3.connect('database.db')
    return conn


def init_db():
    with app.app_context():
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL);''')
        conn.commit()

@app.route('/test_page')
def test_page():
    username = session.get('username')
    user_id = login_window(username)
    return render_template('test_page.html', user_id=user_id)

def login_window(username):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users WHERE username = ?''', (username,))
    user = cursor.fetchone()
    if user:
        return user[1]
    else:
        error = "Ошибка получения имени пользователя"


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
