# models/contract.py
from peewee import ForeignKeyField, DateField, DecimalField, IntegerField
from .base import BaseModel
from .player import Player
from .team import Team

class Contract(BaseModel):
    contract_id = IntegerField(primary_key=True)
    player_id = ForeignKeyField(Player, backref='contracts')
    team_id = ForeignKeyField(Team, backref='contracts')
    start_date = DateField(null=True)
    end_date = DateField(null=True)
    salary = DecimalField(max_digits=15, decimal_places=2, null=True)