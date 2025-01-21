from src.models.base import *

class Teams(Base):
    team_id = IntegerField(primary_key=True)
    team_name = CharField(max_length=100)
    founded_year = IntegerField(null=True)
    stadium = CharField(max_length=100, null=True)