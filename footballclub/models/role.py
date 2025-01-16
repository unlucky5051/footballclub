# models/role.py
from peewee import CharField, IntegerField
from .base import BaseModel

class Role(BaseModel):
    role_id = IntegerField(primary_key=True)
    role_name = CharField(max_length=50)