from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from src.models.users import Users
from src.models.roles import Roles
from src.models.teams import Teams
from src.models.players import Players
from src.models.match import Matches
from src.connect.connect import mysql_db
from peewee import DoesNotExist

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

# API для управления пользователями
@app.route('/api/users', methods=['GET', 'POST'])
def api_users():
    if request.method == 'GET':
        users = Users.select()
        return jsonify([{
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'role_id': user.role_id.role_id,
            'role_name': user.role_id.role_name
        } for user in users])
    elif request.method == 'POST':
        data = request.json
        try:
            user = Users.create(
                username=data['username'],
                password=data['password'],
                email=data['email'],
                role_id=data['role_id']
            )
            return jsonify({
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'role_id': user.role_id.role_id,
                'role_name': user.role_id.role_name
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

@app.route('/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def api_user(user_id):
    try:
        user = Users.get(Users.user_id == user_id)
    except DoesNotExist:
        return jsonify({'error': 'Пользователь не найден'}), 404

    if request.method == 'GET':
        return jsonify({
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'role_id': user.role_id.role_id,
            'role_name': user.role_id.role_name
        })
    elif request.method == 'PUT':
        data = request.json
        user.username = data.get('username', user.username)
        user.password = data.get('password', user.password)
        user.email = data.get('email', user.email)
        user.role_id = data.get('role_id', user.role_id)
        user.save()
        return jsonify({
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'role_id': user.role_id.role_id,
            'role_name': user.role_id.role_name
        })
    elif request.method == 'DELETE':
        user.delete_instance()
        return '', 204

# API для управления командами
@app.route('/api/teams', methods=['GET', 'POST'])
def api_teams():
    if request.method == 'GET':
        teams = Teams.select()
        return jsonify([{
            'team_id': team.team_id,
            'team_name': team.team_name,
            'founded_year': team.founded_year,
            'stadium': team.stadium
        } for team in teams])
    elif request.method == 'POST':
        data = request.json
        try:
            team = Teams.create(
                team_name=data['team_name'],
                founded_year=data.get('founded_year'),
                stadium=data.get('stadium')
            )
            return jsonify({
                'team_id': team.team_id,
                'team_name': team.team_name,
                'founded_year': team.founded_year,
                'stadium': team.stadium
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

@app.route('/api/teams/<int:team_id>', methods=['GET', 'PUT', 'DELETE'])
def api_team(team_id):
    try:
        team = Teams.get(Teams.team_id == team_id)
    except DoesNotExist:
        return jsonify({'error': 'Команда не найдена'}), 404

    if request.method == 'GET':
        return jsonify({
            'team_id': team.team_id,
            'team_name': team.team_name,
            'founded_year': team.founded_year,
            'stadium': team.stadium
        })
    elif request.method == 'PUT':
        data = request.json
        team.team_name = data.get('team_name', team.team_name)
        team.founded_year = data.get('founded_year', team.founded_year)
        team.stadium = data.get('stadium', team.stadium)
        team.save()
        return jsonify({
            'team_id': team.team_id,
            'team_name': team.team_name,
            'founded_year': team.founded_year,
            'stadium': team.stadium
        })
    elif request.method == 'DELETE':
        team.delete_instance()
        return '', 204

# API для управления составом команд
@app.route('/api/teams/<int:team_id>/players', methods=['GET', 'POST'])
def api_team_players(team_id):
    if request.method == 'GET':
        players = Players.select().where(Players.team_id == team_id)
        return jsonify([{
            'player_id': player.player_id,
            'first_name': player.first_name,
            'last_name': player.last_name,
            'date_of_birth': player.date_of_birth,
            'nationality': player.nationality,
            'position': player.position,
            'team_id': player.team_id.team_id
        } for player in players])
    elif request.method == 'POST':
        data = request.json
        try:
            player = Players.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                date_of_birth=data.get('date_of_birth'),
                nationality=data.get('nationality'),
                position=data.get('position'),
                team_id=team_id
            )
            return jsonify({
                'player_id': player.player_id,
                'first_name': player.first_name,
                'last_name': player.last_name,
                'date_of_birth': player.date_of_birth,
                'nationality': player.nationality,
                'position': player.position,
                'team_id': player.team_id.team_id
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

# API для управления игроками
@app.route('/api/players', methods=['GET', 'POST'])
def api_players():
    if request.method == 'GET':
        players = Players.select()
        return jsonify([{
            'player_id': player.player_id,
            'first_name': player.first_name,
            'last_name': player.last_name,
            'date_of_birth': player.date_of_birth,
            'nationality': player.nationality,
            'position': player.position,
            'team_id': player.team_id.team_id
        } for player in players])
    elif request.method == 'POST':
        data = request.json
        try:
            player = Players.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                date_of_birth=data.get('date_of_birth'),
                nationality=data.get('nationality'),
                position=data.get('position'),
                team_id=data['team_id']
            )
            return jsonify({
                'player_id': player.player_id,
                'first_name': player.first_name,
                'last_name': player.last_name,
                'date_of_birth': player.date_of_birth,
                'nationality': player.nationality,
                'position': player.position,
                'team_id': player.team_id.team_id
            }), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

@app.route('/api/players/<int:player_id>', methods=['GET', 'PUT', 'DELETE'])
def api_player(player_id):
    try:
        player = Players.get(Players.player_id == player_id)
    except DoesNotExist:
        return jsonify({'error': 'Игрок не найден'}), 404

    if request.method == 'GET':
        return jsonify({
            'player_id': player.player_id,
            'first_name': player.first_name,
            'last_name': player.last_name,
            'date_of_birth': player.date_of_birth,
            'nationality': player.nationality,
            'position': player.position,
            'team_id': player.team_id.team_id
        })
    elif request.method == 'PUT':
        data = request.json
        player.first_name = data.get('first_name', player.first_name)
        player.last_name = data.get('last_name', player.last_name)
        player.date_of_birth = data.get('date_of_birth', player.date_of_birth)
        player.nationality = data.get('nationality', player.nationality)
        player.position = data.get('position', player.position)
        player.team_id = data.get('team_id', player.team_id)
        player.save()
        return jsonify({
            'player_id': player.player_id,
            'first_name': player.first_name,
            'last_name': player.last_name,
            'date_of_birth': player.date_of_birth,
            'nationality': player.nationality,
            'position': player.position,
            'team_id': player.team_id.team_id
        })
    elif request.method == 'DELETE':
        player.delete_instance()
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)