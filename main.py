import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
import text_bot
from db import SQLither
from parser_stopgame import StopGame
import asyncio
from parser_crackwach_or_API import CrackWatch
from habr_parser import Habr

load_dotenv()  # load .env

TOKEN = str(os.getenv('TG_TOKEN'))  # api token from botfather

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# database
database_stopgame = SQLither('db', 'subscriptions_stopgame')  # init to database
database_crackwatch = SQLither('db', 'subscriptions_crackwatch')
database_habr_python = SQLither('db', 'subscriptions_habr_python')
database_habr_big_data = SQLither('db', 'subscriptions_habr_bigdata')

# parser
parser_stop_game = StopGame('last_key_parser.txt')  # init to parser stopgame
parser_crackwatch = CrackWatch('last_key_crackwatch.txt')
parser_habr_python = Habr(flag='python', file_save='last_post_habr_python.txt')
parser_habr_big_data = Habr(flag='bigdata', file_save='last_post_habr_bigdata.txt')


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.answer(text_bot.HELLO)


@dp.message_handler(commands=['help'])
async def help_bot(message: types.Message):
    await message.answer(text_bot.HELP)


@dp.message_handler(commands=['subscribe_stopgame'])
async def subscribe_user(message: types.Message):
    '''Функция отвечающая за подписку юзера'''
    user_id = str(message.from_user.id)
    if not database_stopgame.subsribe_exists(user_id):
        '''Если юзера нет в БД добавдяем его с активной подпиской'''
        database_stopgame.add_subscriber(user_id, True)
        await  message.answer(text_bot.SUBSCRIBE_NEW)

    else:
        '''иначе присваем юзеру статус подписчика'''
        database_stopgame.update_subscriber(user_id, True)
        await message.answer(text_bot.SUBSCRIBE_OLD)


@dp.message_handler(commands=['unsubscribe_stopgame'])
async def unsubscribe_user(message: types.Message):
    '''Функция отвечающая за отписку юзера'''
    user_id = str(message.from_user.id)
    if not database_stopgame.subsribe_exists(user_id):
        '''Если юзера нет в БД добавдяем его с неактивной подпиской'''
        database_stopgame.add_subscriber(user_id, False)
        await  message.answer(text_bot.UNSUBSCRIBE)

    else:
        '''иначе присваем юзеру статус неподписчика'''
        database_stopgame.update_subscriber(user_id, False)
        await message.answer(text_bot.UNSUBSCRIBE)


@dp.message_handler(commands=['subscribe_crackwatch'])
async def subscribe_user(message: types.Message):
    '''Функция отвечающая за подписку юзера'''
    user_id = str(message.from_user.id)
    if not database_crackwatch.subsribe_exists(user_id):
        '''Если юзера нет в БД добавдяем его с активной подпиской'''
        database_crackwatch.add_subscriber(user_id, True)
        await  message.answer(text_bot.SUBSCRIBE_NEW)

    else:
        '''иначе присваем юзеру статус подписчика'''
        database_crackwatch.update_subscriber(user_id, True)
        await message.answer(text_bot.SUBSCRIBE_OLD)


@dp.message_handler(commands=['unsubscribe_crackwatch'])
async def unsubscribe_user(message: types.Message):
    '''Функция отвечающая за отписку юзера'''
    user_id = str(message.from_user.id)
    if not database_crackwatch.subsribe_exists(user_id):
        '''Если юзера нет в БД добавдяем его с неактивной подпиской'''
        database_crackwatch.add_subscriber(user_id, False)
        await  message.answer(text_bot.UNSUBSCRIBE)

    else:
        '''иначе присваем юзеру статус неподписчика'''
        database_crackwatch.update_subscriber(user_id, False)
        await message.answer(text_bot.UNSUBSCRIBE)


@dp.message_handler(commands=['subscribe_habr_python'])
async def subscribe_user(message: types.Message):
    '''Функция отвечающая за подписку юзера'''
    user_id = str(message.from_user.id)
    if not database_habr_python.subsribe_exists(user_id):
        '''Если юзера нет в БД добавдяем его с активной подпиской'''
        database_habr_python.add_subscriber(user_id, True)
        await  message.answer(text_bot.SUBSCRIBE_NEW)

    else:
        '''иначе присваем юзеру статус подписчика'''
        database_habr_python.update_subscriber(user_id, True)
        await message.answer(text_bot.SUBSCRIBE_OLD)


@dp.message_handler(commands=['unsubscribe_habr_python'])
async def unsubscribe_user(message: types.Message):
    '''Функция отвечающая за отписку юзера'''
    user_id = str(message.from_user.id)
    if not database_habr_python.subsribe_exists(user_id):
        '''Если юзера нет в БД добавдяем его с неактивной подпиской'''
        database_habr_python.add_subscriber(user_id, False)
        await  message.answer(text_bot.UNSUBSCRIBE)

    else:
        '''иначе присваем юзеру статус неподписчика'''
        database_habr_python.update_subscriber(user_id, False)
        await message.answer(text_bot.UNSUBSCRIBE)


@dp.message_handler(commands=['subscribe_habr_bigdata'])
async def subscribe_user(message: types.Message):
    '''Функция отвечающая за подписку юзера'''
    user_id = str(message.from_user.id)
    if not database_habr_big_data.subsribe_exists(user_id):
        '''Если юзера нет в БД добавдяем его с активной подпиской'''
        database_habr_big_data.add_subscriber(user_id, True)
        await  message.answer(text_bot.SUBSCRIBE_NEW)

    else:
        '''иначе присваем юзеру статус подписчика'''
        database_habr_big_data.update_subscriber(user_id, True)
        await message.answer(text_bot.SUBSCRIBE_OLD)


@dp.message_handler(commands=['unsubscribe_habr_bigdata'])
async def unsubscribe_user(message: types.Message):
    '''Функция отвечающая за отписку юзера'''
    user_id = str(message.from_user.id)
    if not database_habr_big_data.subsribe_exists(user_id):
        '''Если юзера нет в БД добавдяем его с неактивной подпиской'''
        database_habr_big_data.add_subscriber(user_id, False)
        await  message.answer(text_bot.UNSUBSCRIBE)

    else:
        '''иначе присваем юзеру статус неподписчика'''
        database_habr_big_data.update_subscriber(user_id, False)
        await message.answer(text_bot.UNSUBSCRIBE)


# асинхронная функция которая проверяет наличие игр
async def main_malling_stop_game(time_wait):
    while True:
        await asyncio.sleep(time_wait)
        print('s')
        parser_stop_game.clear()  # очищаем список с ссылками
        new_games = parser_stop_game.new_game_href()
        if new_games:  # если появились новые обзоры на сайте
            new_games.reverse()
            for game in new_games:
                info = parser_stop_game.parse_game_info(game)  # парсим данные игры
                subsciptions = database_stopgame.get_subscriptions()  # получаем текущих подписчиков
                parser_stop_game.download_image(info.poster)
                print(info)
                with open('img_stop_game.jpg', 'rb') as photo:
                    for i in subsciptions:
                        await bot.send_photo(  # отправляем подписчикам инфу об игре
                            i[1],
                            photo,
                            caption=info.title + "\n" + "Оценка: " + info.score + "\n" + info.text + "\n\n" + info.href,
                            disable_notification=True
                        )
                        parser_stop_game.update_last_key(parser_stop_game.parse_href(info.href))  # изменяем ключ игры


async def main_malling_crackwatch(time_wait):
    while True:
        await asyncio.sleep(time_wait)
        result_crackwatch = parser_crackwatch.new_game()
        if result_crackwatch:
            subsciptions = database_crackwatch.get_subscriptions()  # получаем текущих подписчиков
            parser_crackwatch.download_image(result_crackwatch.image)
            with open('img_crackwatch.jpg', 'rb') as photo:
                for i in subsciptions:
                    await bot.send_photo(
                        i[1],
                        photo,
                        caption=result_crackwatch.title + '\n' + 'Защита: ' + result_crackwatch.protections + '\n' + \
                                'Группа взломщиков:' + result_crackwatch.groups + '\n' + 'Игра вышла: ' + \
                                result_crackwatch.releaseDate + '\n' + 'Взломана: ' + result_crackwatch.crackDate + \
                                '\n' + result_crackwatch.href
                        ,
                        disable_notification=True
                    )


async def mail_malling_habr_python(time_wait):
    while True:
        await asyncio.sleep(time_wait)
        result_habr = 1


async def mail_malling_habr_big_data(time_wait):
    while True:
        await asyncio.sleep(time_wait)
        result_habr = 1


if __name__ == '__main__':
    # database_stopgame.check_database()  # проверяем существует ли БД
    dp.loop.create_task(main_malling_stop_game(30))  # запускаем асинхронную функцию
    dp.loop.create_task(main_malling_crackwatch(30))
    executor.start_polling(dp, skip_updates=True)
