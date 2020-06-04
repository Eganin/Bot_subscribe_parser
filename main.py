import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
import text_bot
from db import SQLither
from parser_stopgame import StopGame
import asyncio

load_dotenv()  # load .env

TOKEN = str(os.getenv('TG_TOKEN'))  # api token from botfather

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

database = SQLither('db')  # init to database

parser = StopGame('last_key_parser.txt')  # init to parser


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.answer(text_bot.HELLO)


@dp.message_handler(commands=['help'])
async def help_bot(message: types.Message):
    await message.answer(text_bot.HELP)


@dp.message_handler(commands=['subscribe'])
async def subscribe_user(message: types.Message):
    '''Функция отвечающая за подписку юзера'''
    user_id = str(message.from_user.id)
    if not database.subsribe_exists(user_id):
        '''Если юзера нет в БД добавдяем его с активной подпиской'''
        database.add_subscriber(user_id, True)
        database.close()  # закрытие соединения с БД
        await  message.answer(text_bot.SUBSCRIBE_NEW)

    else:
        '''иначе присваем юзеру статус подписчика'''
        database.update_subscriber(user_id, True)
        database.close()
        await message.answer(text_bot.SUBSCRIBE_OLD)


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe_user(message: types.Message):
    '''Функция отвечающая за отписку юзера'''
    user_id = str(message.from_user.id)
    if not database.subsribe_exists(user_id):
        '''Если юзера нет в БД добавдяем его с неактивной подпиской'''
        database.add_subscriber(user_id, False)
        database.close()
        await  message.answer(text_bot.UNSUBSCRIBE)

    else:
        '''иначе присваем юзеру статус неподписчика'''
        database.update_subscriber(user_id, False)
        database.close()
        await message.answer(text_bot.UNSUBSCRIBE)


# асинхронная функция которая проверяет наличие игр
async def main_malling(time_wait):
    while True:
        await asyncio.sleep(time_wait)
        parser.clear()  # очищаем список с ссылками
        new_games = parser.new_game_href()
        if new_games:  # если появились новые обзоры на сайте
            new_games.reverse()
            for game in new_games:
                info = parser.parse_game_info(game)  # парсим данные игры
                subsciptions = database.get_subscriptions()  # получаем текущих подписчиков
                parser.download_image(info.poster)
                with open('img.jpg', 'rb') as photo:
                    for i in subsciptions:
                        await bot.send_photo(  # отправляем подписчикам инфу об игре
                            i[1],
                            photo,
                            caption=info.title + "\n" + "Оценка: " + info.score + "\n" + info.text + "\n\n" + info.href,
                            disable_notification=True
                        )
                        parser.update_last_key(parser.parse_href(info.href))  # изменяем ключ игры


if __name__ == '__main__':
    database.check_database()  # проверяем существует ли БД
    dp.loop.create_task(main_malling(30))  # запускаем асинхронную функцию
    executor.start_polling(dp, skip_updates=True)
