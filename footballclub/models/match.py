# models/match.py
from peewee import ForeignKeyField, DateField, CharField, IntegerField
from .base import BaseModel
from .team import Team

class Match(BaseModel):
    match_id = IntegerField(primary_key=True)
    match_date = DateField(null=True)
    home_team_id = ForeignKeyField(Team, backref='home_matches')
    away_team_id = ForeignKeyField(Team, backref='away_matches')
    tournament_id = IntegerField(null=True)
    score = CharField(max_length=10, null=True)