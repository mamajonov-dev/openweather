from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup
import sqlite3

def generatesavecitybutton(cityname):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Shaharni saqlash', callback_data=f'save_{cityname}'))
    return markup


def generatecitiesmenu(chat_id):

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()

    cursor.execute('''SELECT city_name FROM cities WHERE telegram_id = ?''', (chat_id, ))

    cities = cursor.fetchall()

    for city in cities:
        markup.add(KeyboardButton(text=city[0]))

    return markup
