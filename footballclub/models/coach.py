# models/coach.py
from peewee import ForeignKeyField, CharField, DateField, IntegerField
from .base import BaseModel
from .team import Team
from .user import User

class Coach(BaseModel):
    coach_id = IntegerField(primary_key=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    date_of_birth = DateField(null=True)
    nationality = CharField(max_length=50, null=True)
    team_id = ForeignKeyField(Team, backref='coaches', null=True)
    user_id = ForeignKeyField(User, backref='coaches', unique=True, null=True)