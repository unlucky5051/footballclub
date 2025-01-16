# models/player.py
from peewee import ForeignKeyField, CharField, DateField, IntegerField
from .base import BaseModel
from .team import Team
from .user import User

class Player(BaseModel):
    player_id = IntegerField(primary_key=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    date_of_birth = DateField(null=True)
    nationality = CharField(max_length=50, null=True)
    position = CharField(max_length=50, null=True)
    team_id = ForeignKeyField(Team, backref='players', null=True)
    user_id = ForeignKeyField(User, backref='players', unique=True, null=True)