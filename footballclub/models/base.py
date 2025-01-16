
from peewee import MySQLDatabase, Model

# Подключение к базе данных
db = MySQLDatabase('fkzenut', user='username', password='password', host='localhost', port=3306)

class BaseModel(Model):
    class Meta:
        database = db