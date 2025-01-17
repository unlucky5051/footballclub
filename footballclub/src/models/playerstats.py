from src.models.base import *
from src.models.players import *
from src.models.match import *

class PlayerStats(Base):
    stat_id = IntegerField(primary_key=True)
    player_id = ForeignKeyField(Players, backref='player_stats')
    match_id = ForeignKeyField(Matches, backref='player_stats')
    goals = IntegerField(null=True)
    assists = IntegerField(null=True)
    yellow_cards = IntegerField(null=True)
    red_cards = IntegerField(null=True)