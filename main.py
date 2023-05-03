from aiogram import Bot, Dispatcher, executor
import os
from aiogram.types import Message, CallbackQuery
import sqlite3
from dotenv import load_dotenv
load_dotenv()



from keyboards import generatesavecitybutton, generatecitiesmenu
from openweather import getweatherinfo

bot = Bot(os.getenv('telegram'))
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: Message):
    chatid = message.chat.id
    await message.answer('Xush kelibsiz ', reply_markup=generatecitiesmenu(str(chatid)))
    await registruser(message)

async def registruser(message: Message):
    fullname = message.from_user.full_name
    telegramid = message.chat.id
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()
    try:
        cursor.execute('''INSERT INTO users(fullname, telegramid)
        VALUES (?, ?)''', (fullname, telegramid))
        database.commit()
        database.close()

    except:
        await message.answer('Qaytganingizdan xursandmiz. Shaxar nomini kiriting')


@dp.message_handler()
async def getcity(message: Message):
    city = message.text.title()
    text = getweatherinfo(city)
    text, image = text

    await message.answer_photo(photo=image, caption=text, reply_markup=generatesavecitybutton(city))
    # await bot.send_photo(message.chat.id, photo=image, caption=text)

@dp.callback_query_handler(lambda call: 'save' in call.data)
async def savecity(call: CallbackQuery):
    telegramid = call.message.chat.id
    i, city = call.data.split('_')
    database = sqlite3.connect('database.sqlite')
    cursor = database.cursor()

    cursor.execute('''SELECT telegramid FROM users WHERE telegramid = ?''', (telegramid, ))
    chat_id = cursor.fetchone()[0]
    cursor.execute('''INSERT INTO cities(city_name, telegram_id)
    VALUES (?, ?)''', (city, chat_id))
    database.commit()
    database.close()
    await bot.send_message(chat_id, 'Shaxar saqlandi', reply_markup=generatecitiesmenu(chat_id))
executor.start_polling(dp, skip_updates=True)