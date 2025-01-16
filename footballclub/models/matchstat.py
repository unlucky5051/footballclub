# models/matchstat.py
from peewee import ForeignKeyField, IntegerField
from .base import BaseModel
from .match import Match

class MatchStat(BaseModel):
    match_stat_id = IntegerField(primary_key=True)
    match_id = ForeignKeyField(Match, backref='match_stats')
    possession_home = IntegerField(null=True)
    possession_away = IntegerField(null=True)
    shots_on_target_home = IntegerField(null=True)
    shots_on_target_away = IntegerField(null=True)
    fouls_home = IntegerField(null=True)
    fouls_away = IntegerField(null=True)