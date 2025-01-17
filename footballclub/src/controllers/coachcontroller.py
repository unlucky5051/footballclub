# coachcontroller.py
from src.models.players import Players
from src.models.teams import Teams
from peewee import DoesNotExist

class CoachController:
    @staticmethod
    def get_players_by_team(team_id):
        """
        Возвращает список игроков по team_id.
        В случае ошибки возвращает пустой список.
        """
        try:
            players = Players.select().where(Players.team_id == team_id)
            return list(players)
        except Exception as e:
            print(f"Ошибка при получении списка игроков: {e}")
            return []

    @staticmethod
    def add_player_to_team(team_id, first_name, last_name, date_of_birth=None, nationality=None, position=None, user_id=None):
        """
        Добавляет нового игрока в команду по team_id.
        Возвращает созданного игрока или None в случае ошибки.
        """
        try:
            team = Teams.get(Teams.team_id == team_id)
            player = Players.create(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                nationality=nationality,
                position=position,
                team_id=team,
                user_id=user_id
            )
            print(f"Игрок {first_name} {last_name} успешно добавлен в команду {team.team_name}.")
            return player
        except DoesNotExist:
            print(f"Команда с ID {team_id} не найдена.")
            return None
        except Exception as e:
            print(f"Ошибка при добавлении игрока: {e}")
            return None

    @staticmethod
    def update_player(player_id, first_name=None, last_name=None, date_of_birth=None, nationality=None, position=None, team_id=None):
        """
        Обновляет данные игрока по player_id.
        Возвращает обновленного игрока или None в случае ошибки.
        """
        try:
            player = Players.get(Players.player_id == player_id)
            if first_name:
                player.first_name = first_name
            if last_name:
                player.last_name = last_name
            if date_of_birth:
                player.date_of_birth = date_of_birth
            if nationality:
                player.nationality = nationality
            if position:
                player.position = position
            if team_id:
                team = Teams.get(Teams.team_id == team_id)
                player.team_id = team
            player.save()
            print(f"Данные игрока с ID {player_id} успешно обновлены.")
            return player
        except DoesNotExist:
            print(f"Игрок с ID {player_id} или команда с ID {team_id} не найдены.")
            return None
        except Exception as e:
            print(f"Ошибка при обновлении данных игрока: {e}")
            return None

    @staticmethod
    def delete_player(player_id):
        """
        Удаляет игрока по player_id.
        Возвращает True, если удаление прошло успешно, иначе False.
        """
        try:
            player = Players.get(Players.player_id == player_id)
            player.delete_instance()
            print(f"Игрок с ID {player_id} успешно удален.")
            return True
        except DoesNotExist:
            print(f"Игрок с ID {player_id} не найден.")
            return False
        except Exception as e:
            print(f"Ошибка при удалении игрока: {e}")
            return False

if __name__ == "__main__":
    # Пример использования
    # Получение списка игроков команды
    players = CoachController.get_players_by_team(1)
    for player in players:
        print(f"{player.first_name} {player.last_name}")

    # Добавление нового игрока
    new_player = CoachController.add_player_to_team(
        team_id=1,
        first_name="Иван",
        last_name="Иванов",
        date_of_birth="1990-01-01",
        nationality="Россия",
        position="Нападающий"
    )

    # Обновление данных игрока
    updated_player = CoachController.update_player(
        player_id=1,
        first_name="Петр",
        last_name="Петров",
        position="Полузащитник"
    )
