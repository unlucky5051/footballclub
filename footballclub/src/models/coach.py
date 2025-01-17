from src.models.base import *
from src.models.teams import Team
from src.models.users import User


class Coach(Base):
    coach_id = IntegerField(primary_key=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    date_of_birth = DateField(null=True)
    nationality = CharField(max_length=50, null=True)
    team_id = ForeignKeyField(Team, backref='coaches', null=True)
    user_id = ForeignKeyField(User, backref='coaches', unique=True, null=True)