from src.models.base import *

class Roles(Base):
    role_id = IntegerField(primary_key=True)
    role_name = CharField(max_length=50)