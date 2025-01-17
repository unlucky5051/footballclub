from src.models.base import *
from src.models.teams import *
from src.models.users import *


class Players(Base):
    player_id = IntegerField(primary_key=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    date_of_birth = DateField(null=True)
    nationality = CharField(max_length=50, null=True)
    position = CharField(max_length=50, null=True)
    team_id = ForeignKeyField(Teams, backref='players', null=True)
    user_id = ForeignKeyField(Users, backref='players', unique=True, null=True)