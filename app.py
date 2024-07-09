from flask import Flask, render_template, url_for, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'tribnribnien3iu43bnu3ib53u'
check_list = ['First', 'Second', 'Third']

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

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

@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # получение даннных из формы регистрации
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        if password != password_confirm:
            return render_template('reg.html', error="Пароли не совпадают")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256') # хешируем пароль
        db = db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,)) # тут ищем нет ли уже такого юзера в бд
        user = cursor.fetchone() # получаем результат запроса
        if user:
            return render_template('reg.html', error="Пользователь уже существует") # показать стр. регистрации с ошибкой
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            db.commit()
            return redirect(url_for('login'))
    return render_template('reg.html')

@app.route('/login', methods = ['GET', 'POST'])
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



if __name__ == '__main__':
    init_db()
    app.run(debug=True)
