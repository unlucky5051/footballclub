# models/user.py
from peewee import ForeignKeyField, CharField, IntegerField
from .base import BaseModel
from .role import Role

class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    username = CharField(unique=True, max_length=50)
    password = CharField(max_length=100)
    email = CharField(unique=True, max_length=100)
    role_id = ForeignKeyField(Role, backref='users')