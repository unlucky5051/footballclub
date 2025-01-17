# usercontroller.py
from src.models.teams import Teams
from src.models.match import Matches
from src.models.matchstat import MatchStats
from src.models.playerstats import PlayerStats
from peewee import DoesNotExist

class UserController:
    @staticmethod
    def get_team_stats():
        """
        Возвращает статистику всех команд за все матчи.
        В случае ошибки возвращает пустой список.
        """
        try:
            team_stats = MatchStats.select()
            return list(team_stats)
        except Exception as e:
            print(f"Ошибка при получении статистики команд: {e}")
            return []

    @staticmethod
    def get_all_player_stats():
        """
        Возвращает статистику всех игроков.
        В случае ошибки возвращает пустой список.
        """
        try:
            player_stats = PlayerStats.select()
            return list(player_stats)
        except Exception as e:
            print(f"Ошибка при получении статистики игроков: {e}")
            return []

    @staticmethod
    def get_upcoming_matches():
        """
        Возвращает список предстоящих матчей с указанием команд.
        В случае ошибки возвращает пустой список.
        """
        try:
            upcoming_matches = Matches.select().where(Matches.match_date >= "2023-10-01")  # Пример даты для фильтрации будущих матчей
            matches_info = []
            for match in upcoming_matches:
                home_team = Teams.get(Teams.team_id == match.home_team_id)
                away_team = Teams.get(Teams.team_id == match.away_team_id)
                matches_info.append({
                    "match_id": match.match_id,
                    "match_date": match.match_date,
                    "home_team": home_team.team_name,
                    "away_team": away_team.team_name,
                    "tournament_id": match.tournament_id
                })
            return matches_info
        except Exception as e:
            print(f"Ошибка при получении предстоящих матчей: {e}")
            return []

    @staticmethod
    def get_past_matches():
        """
        Возвращает список завершенных матчей с указанием команд.
        В случае ошибки возвращает пустой список.
        """
        try:
            past_matches = Matches.select().where(Matches.match_date < "2023-10-01")  # Пример даты для фильтрации прошлых матчей
            matches_info = []
            for match in past_matches:
                home_team = Teams.get(Teams.team_id == match.home_team_id)
                away_team = Teams.get(Teams.team_id == match.away_team_id)
                matches_info.append({
                    "match_id": match.match_id,
                    "match_date": match.match_date,
                    "home_team": home_team.team_name,
                    "away_team": away_team.team_name,
                    "score": match.score,
                    "tournament_id": match.tournament_id
                })
            return matches_info
        except Exception as e:
            print(f"Ошибка при получении завершенных матчей: {e}")
            return []

if __name__ == "__main__":
    # Пример использования
    # Получение статистики команд
    team_stats = UserController.get_team_stats()
    for stat in team_stats:
        print(f"Матч {stat.match_id}: Владение дома - {stat.possession_home}%, Владение в гостях - {stat.possession_away}%")

    # Получение статистики всех игроков
    player_stats = UserController.get_all_player_stats()
    for stat in player_stats:
        print(f"Игрок {stat.player_id}: Голы - {stat.goals}, Ассисты - {stat.assists}")

    # Получение предстоящих матчей
    upcoming_matches = UserController.get_upcoming_matches()
    for match in upcoming_matches:
        print(f"Предстоящий матч: {match['match_date']}, {match['home_team']} vs {match['away_team']}")

    # Получение завершенных матчей
    past_matches = UserController.get_past_matches()
    for match in past_matches:
        print(f"Завершенный матч: {match['match_date']}, {match['home_team']} {match['score']} {match['away_team']}")