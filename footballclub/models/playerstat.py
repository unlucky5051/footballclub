# models/playerstat.py
from peewee import ForeignKeyField, IntegerField
from .base import BaseModel
from .player import Player
from .match import Match

class PlayerStat(BaseModel):
    stat_id = IntegerField(primary_key=True)
    player_id = ForeignKeyField(Player, backref='player_stats')
    match_id = ForeignKeyField(Match, backref='player_stats')
    goals = IntegerField(null=True)
    assists = IntegerField(null=True)
    yellow_cards = IntegerField(null=True)
    red_cards = IntegerField(null=True)