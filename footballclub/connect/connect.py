from peewee import *

# Подключение к базе данных на локальном сервере
mysql_db = MySQLDatabase('FKzenut', user='unlucky', password = '11111', host='127.0.0.1', port=3306)

if __name__ == "__main__":
    mysql_db.connect()
    print("Соединение с базой данных установлено")