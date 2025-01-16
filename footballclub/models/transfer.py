# models/transfer.py
from peewee import ForeignKeyField, DateField, DecimalField, IntegerField
from .base import BaseModel
from .player import Player
from .team import Team

class Transfer(BaseModel):
    transfer_id = IntegerField(primary_key=True)
    player_id = ForeignKeyField(Player, backref='transfers')
    from_team_id = ForeignKeyField(Team, backref='transfers_from')
    to_team_id = ForeignKeyField(Team, backref='transfers_to')
    transfer_date = DateField(null=True)
    transfer_fee = DecimalField(max_digits=15, decimal_places=2, null=True)