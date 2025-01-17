from src.models.base import *
from src.models.players import Player
from src.models.teams import Team


class Contract(Base):
    contract_id = IntegerField(primary_key=True)
    player_id = ForeignKeyField(Player, backref='contracts')
    team_id = ForeignKeyField(Team, backref='contracts')
    start_date = DateField(null=True)
    end_date = DateField(null=True)
    salary = DecimalField(max_digits=15, decimal_places=2, null=True)