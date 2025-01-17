from peewee import *

# Подключение к базе данных на локальном сервере
mysql_db = MySQLDatabase('ZHuV1234_FKzenut', user='ZHuV1234_ball', password = '111111', host='10.11.13.118', port=3306)

if __name__ == "__main__":
    mysql_db.connect()
    print("Соединение с базой данных установлено")