import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
import text_bot
from db import SQLither
from parser import StopGame
import asyncio

load_dotenv()  # load .env

TOKEN = str(os.getenv('TG_TOKEN'))  # api token from botfather

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

database = SQLither('db')  # init to database

parser = StopGame('last_href_parser.txt')


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    print(message.from_user.id)
    await message.answer(text_bot.HELLO)


@dp.message_handler(commands=['help'])
async def help_bot(message: types.Message):
    await message.answer(text_bot.HELP)


@dp.message_handler(commands=['subscribe'])
async def subscribe_user(message: types.Message):
    user_id = str(message.from_user.id)
    if not database.subsribe_exists(user_id):
        '''Если юзера нет в БД добавдяем его с активной подпиской'''
        database.add_subscriber(user_id, True)
        await  message.answer(text_bot.SUBSCRIBE_NEW)

    else:
        '''иначе присваем юзеру статус подписчика'''
        database.update_subscriber(user_id, True)
        await message.answer(text_bot.SUBSCRIBE_OLD)


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe_user(message: types.Message):
    user_id = str(message.from_user.id)
    if not database.subsribe_exists(user_id):
        '''Если юзера нет в БД добавдяем его с неактивной подпиской'''
        database.add_subscriber(user_id, False)
        await  message.answer(text_bot.UNSUBSCRIBE)

    else:
        '''иначе присваем юзеру статус неподписчика'''
        database.update_subscriber(user_id, False)
        await message.answer(text_bot.UNSUBSCRIBE)


# асинхронная функция которая проверяет наличие игр
async def main_malling(time_wait):
    while True:
        await asyncio.sleep(time_wait)
        print('letsgo')
        new_games = parser.new_game_href()
        if new_games:
            new_games.reverse()
            for game in new_games:
                info = parser.parse_game_info(game)
                subsciptions = database.get_subscriptions()
                parser.download_image(info[0])
                with open('img.jpg', 'rb') as photo:
                    for i in subsciptions:
                        await bot.send_photo(
                            i[1],
                            photo,
                            caption=info[3] + "\n" + "Оценка: " + info[2] + "\n" + info[1] + "\n\n" + info[4],
                            disable_notification=True
                        )


if __name__ == '__main__':
    dp.loop.create_task(main_malling(30))
    executor.start_polling(dp, skip_updates=True)
