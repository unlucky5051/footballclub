from flask import Flask, render_template, request, redirect, url_for, session
from src.models.users import Users
from src.models.roles import Roles
from src.models.teams import Teams
from src.models.players import Players
from src.models.match import Matches
from src.connect.connect import mysql_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Секретный ключ для сессий

# Подключение к базе данных
mysql_db.connect()

@app.route('/')
def home():
    # Получаем информацию о команде, игроках и матчах
    try:
        team = Teams.get(Teams.team_id == 1)  # Пример: получаем команду с ID 1
        players = Players.select().where(Players.team_id == 1)  # Получаем игроков команды
        matches = Matches.select().where((Matches.home_team_id == 1) | (Matches.away_team_id == 1))  # Получаем матчи команды
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        team = None
        players = []
        matches = []

    return render_template('home.html', team=team, players=players, matches=matches)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            user = Users.get(Users.username == username, Users.password == password)
            session['user_id'] = user.user_id
            session['role_id'] = user.role_id.role_id

            # Перенаправление в зависимости от роли
            if user.role_id.role_id == 1:  # Администратор
                return redirect(url_for('admin_panel'))
            elif user.role_id.role_id == 2:  # Тренер
                return redirect(url_for('coach_panel'))
            elif user.role_id.role_id == 3:  # Игрок
                return redirect(url_for('player_panel'))
        except Users.DoesNotExist:
            return "Неверное имя пользователя или пароль", 401

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role_id = request.form['role_id']

        try:
            user = Users.create(username=username, password=password, email=email, role_id=role_id)
            return redirect(url_for('login'))
        except Exception as e:
            return f"Ошибка при регистрации: {e}", 400

    return render_template('register.html')

@app.route('/admin')
def admin_panel():
    if 'user_id' not in session or session['role_id'] != 1:
        return redirect(url_for('login'))
    return render_template('adminpanel.html')

@app.route('/coach')
def coach_panel():
    if 'user_id' not in session or session['role_id'] != 2:
        return redirect(url_for('login'))
    return render_template('coachpanel.html')

@app.route('/player')
def player_panel():
    if 'user_id' not in session or session['role_id'] != 3:
        return redirect(url_for('login'))
    return render_template('playerpanel.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)