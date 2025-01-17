from src.models.base import *
from src.models.match import *

class MatchStats(Base):
    match_stat_id = IntegerField(primary_key=True)
    match_id = ForeignKeyField(Matches, backref='match_stats')
    possession_home = IntegerField(null=True)
    possession_away = IntegerField(null=True)
    shots_on_target_home = IntegerField(null=True)
    shots_on_target_away = IntegerField(null=True)
    fouls_home = IntegerField(null=True)
    fouls_away = IntegerField(null=True)