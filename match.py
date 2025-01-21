from src.models.base import *
from src.models.teams import Teams


class Matches(Base):
    match_id = IntegerField(primary_key=True)
    match_date = DateField(null=True)
    home_team_id = ForeignKeyField(Teams, backref='home_matches')
    away_team_id = ForeignKeyField(Teams, backref='away_matches')
    tournament_id = IntegerField(null=True)
    score = CharField(max_length=10, null=True)