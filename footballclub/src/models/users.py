from src.models.base import *
from src.models.roles import *

class Users(Base):
    user_id = IntegerField(primary_key=True)
    username = CharField(unique=True, max_length=50)
    password = CharField(max_length=100)
    email = CharField(unique=True, max_length=100)
    role_id = ForeignKeyField(Roles, backref='users')