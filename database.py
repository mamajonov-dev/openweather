import sqlite3

def createuserstable():
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()

    cursor.execute('''CREATE TABLE users (
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(50),
    telegramid INTEGER UNIQUE
    )''')


def createcitiestable():
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE cities(
    city_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name VARCHAR(100),
    telegram_id INTEGER REFERENCES users(telegramid)
    )''')


