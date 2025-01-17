# playercontroller.py
from src.models.players import *
from src.models.teams import *
from src.models.match import *
from src.models.playerstats import PlayerStats
from peewee import DoesNotExist

class PlayerController:
    @staticmethod
    def get_player_stats(player_id):
        """
        Возвращает статистику игрока по player_id.
        В случае ошибки возвращает пустой список.
        """
        try:
            stats = PlayerStats.select().where(PlayerStats.player_id == player_id)
            return list(stats)
        except Exception as e:
            print(f"Ошибка при получении статистики игрока: {e}")
            return []

    @staticmethod
    def get_other_player_stats(player_id):
        """
        Возвращает статистику всех игроков, кроме указанного player_id.
        В случае ошибки возвращает пустой список.
        """
        try:
            stats = PlayerStats.select().where(PlayerStats.player_id != player_id)
            return list(stats)
        except Exception as e:
            print(f"Ошибка при получении статистики других игроков: {e}")
            return []

    @staticmethod
    def get_team_info(team_id):
        """
        Возвращает информацию о команде по team_id.
        В случае ошибки возвращает None.
        """
        try:
            team = Teams.get(Teams.team_id == team_id)
            return team
        except DoesNotExist:
            print(f"Команда с ID {team_id} не найдена.")
            return None
        except Exception as e:
            print(f"Ошибка при получении информации о команде: {e}")
            return None

    @staticmethod
    def get_other_teams_info():
        """
        Возвращает информацию о всех командах, кроме команды текущего игрока.
        В случае ошибки возвращает пустой список.
        """
        try:
            teams = Teams.select()
            return list(teams)
        except Exception as e:
            print(f"Ошибка при получении информации о командах: {e}")
            return []

    @staticmethod
    def get_past_matches(team_id):
        """
        Возвращает список завершенных матчей для команды по team_id.
        В случае ошибки возвращает пустой список.
        """
        try:
            past_matches = Matches.select().where(
                (Matches.home_team_id == team_id) | (Matches.away_team_id == team_id),
                Matches.match_date < "2023-10-01"  # Пример даты для фильтрации прошлых матчей
            )
            return list(past_matches)
        except Exception as e:
            print(f"Ошибка при получении завершенных матчей: {e}")
            return []

    @staticmethod
    def get_upcoming_matches(team_id):
        """
        Возвращает список будущих матчей для команды по team_id.
        В случае ошибки возвращает пустой список.
        """
        try:
            upcoming_matches = Matches.select().where(
                (Matches.home_team_id == team_id) | (Matches.away_team_id == team_id),
                Matches.match_date >= "2023-10-01"  # Пример даты для фильтрации будущих матчей
            )
            return list(upcoming_matches)
        except Exception as e:
            print(f"Ошибка при получении будущих матчей: {e}")
            return []

if __name__ == "__main__":
    # Пример использования
    player_id = 1
    team_id = 1

    # Получение статистики игрока
    player_stats = PlayerController.get_player_stats(player_id)
    for stat in player_stats:
        print(f"Игрок {stat.player_id}: Голы - {stat.goals}, Ассисты - {stat.assists}")

    # Получение статистики других игроков
    other_player_stats = PlayerController.get_other_player_stats(player_id)
    for stat in other_player_stats:
        print(f"Игрок {stat.player_id}: Голы - {stat.goals}, Ассисты - {stat.assists}")

    # Получение информации о команде
    team_info = PlayerController.get_team_info(team_id)
    if team_info:
        print(f"Команда: {team_info.team_name}, Стадион: {team_info.stadium}")

    # Получение информации о других командах
    other_teams = PlayerController.get_other_teams_info()
    for team in other_teams:
        print(f"Команда: {team.team_name}, Год основания: {team.founded_year}")

    # Получение завершенных матчей
    past_matches = PlayerController.get_past_matches(team_id)
    for match in past_matches:
        print(f"Завершенный матч: {match.match_date}, Счет: {match.score}")

    # Получение будущих матчей
    upcoming_matches = PlayerController.get_upcoming_matches(team_id)
    for match in upcoming_matches:
        print(f"Будущий матч: {match.match_date}, Счет: {match.score}")