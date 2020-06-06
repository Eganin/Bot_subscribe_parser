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
from parser_tproger import Tproger
import exceptions

load_dotenv()  # load .env

TOKEN = str(os.getenv('TG_TOKEN'))  # api token from botfather

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# database
database_stopgame = SQLither('datasql', 'subscriptions_stopgame')  # init to database
database_crackwatch = SQLither('datasql', 'subscriptions_crackwatch')
database_habr_python = SQLither('datasql', 'subscriptions_habr_python')
database_habr_big_data = SQLither('datasql', 'subscriptions_habr_bigdata')
database_tproger = SQLither('datasql', 'subscriptions_tproger')

# parser
parser_stop_game = StopGame('last_key_parser.txt')  # init to parser stopgame
parser_crackwatch = CrackWatch('last_key_crackwatch.txt')
parser_habr_python = Habr(flag='python', file_save='last_post_habr_python.txt')
parser_habr_big_data = Habr(flag='bigdata', file_save='last_post_habr_bigdata.txt')
parser_tproger = Tproger('last_key_tpoger.txt')


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message) -> None:
    await message.answer(text_bot.HELLO)


@dp.message_handler(commands=['help'])
async def help_bot(message: types.Message) -> None:
    await message.answer(text_bot.HELP)


@dp.message_handler(commands=['subscribe_stopgame'])
async def subscribe_user(message: types.Message) -> None:
    '''Функция отвечающая за подписку юзера на рассылку stopgame'''
    user_id = str(message.from_user.id)
    try:
        if not database_stopgame.subsribe_exists(user_id):
            '''Если юзера нет в БД добавдяем его с активной подпиской'''
            database_stopgame.add_subscriber(user_id, True)
            await  message.answer(text_bot.SUBSCRIBE_NEW)

        else:
            '''иначе присваем юзеру статус подписчика'''
            database_stopgame.update_subscriber(user_id, True)
            await message.answer(text_bot.SUBSCRIBE_OLD)

    except:
        raise exceptions.ErrorConnectToDB(await message.answer('Произошла ошибка подключения к базе данных'))


@dp.message_handler(commands=['unsubscribe_stopgame'])
async def unsubscribe_user(message: types.Message) -> None:
    '''Функция отвечающая за отписку юзера на рассылку stopgame'''
    user_id = str(message.from_user.id)
    try:
        if not database_stopgame.subsribe_exists(user_id):
            '''Если юзера нет в БД добавдяем его с неактивной подпиской'''
            database_stopgame.add_subscriber(user_id, False)
            await  message.answer(text_bot.UNSUBSCRIBE)

        else:
            '''иначе присваем юзеру статус неподписчика'''
            database_stopgame.update_subscriber(user_id, False)
            await message.answer(text_bot.UNSUBSCRIBE)

    except:
        raise exceptions.ErrorConnectToDB(await message.answer('Произошла ошибка подключения к базе данных'))


@dp.message_handler(commands=['subscribe_crackwatch'])
async def subscribe_user(message: types.Message) -> None:
    '''Функция отвечающая за подписку юзера на рассылку crackwatch'''
    user_id = str(message.from_user.id)
    try:
        if not database_crackwatch.subsribe_exists(user_id):
            '''Если юзера нет в БД добавдяем его с активной подпиской'''
            database_crackwatch.add_subscriber(user_id, True)
            await  message.answer(text_bot.SUBSCRIBE_NEW)

        else:
            '''иначе присваем юзеру статус подписчика'''
            database_crackwatch.update_subscriber(user_id, True)
            await message.answer(text_bot.SUBSCRIBE_OLD)

    except:
        raise exceptions.ErrorConnectToDB(await message.answer('Произошла ошибка подключения к базе данных'))


@dp.message_handler(commands=['unsubscribe_crackwatch'])
async def unsubscribe_user(message: types.Message) -> None:
    '''Функция отвечающая за отписку юзера на расссылку crackwatch'''
    user_id = str(message.from_user.id)
    try:
        if not database_crackwatch.subsribe_exists(user_id):
            '''Если юзера нет в БД добавдяем его с неактивной подпиской'''
            database_crackwatch.add_subscriber(user_id, False)
            await  message.answer(text_bot.UNSUBSCRIBE)

        else:
            '''иначе присваем юзеру статус неподписчика'''
            database_crackwatch.update_subscriber(user_id, False)
            await message.answer(text_bot.UNSUBSCRIBE)

    except:
        raise exceptions.ErrorConnectToDB(await message.answer('Произошла ошибка подключения к базе данных'))


@dp.message_handler(commands=['subscribe_habr_python'])
async def subscribe_user(message: types.Message) -> None:
    '''Функция отвечающая за подписку юзера на рассылку habr python'''
    user_id = str(message.from_user.id)
    try:
        if not database_habr_python.subsribe_exists(user_id):
            '''Если юзера нет в БД добавдяем его с активной подпиской'''
            database_habr_python.add_subscriber(user_id, True)
            await  message.answer(text_bot.SUBSCRIBE_NEW)

        else:
            '''иначе присваем юзеру статус подписчика'''
            database_habr_python.update_subscriber(user_id, True)
            await message.answer(text_bot.SUBSCRIBE_OLD)

    except:
        raise exceptions.ErrorConnectToDB(await message.answer('Произошла ошибка подключения к базе данных'))


@dp.message_handler(commands=['unsubscribe_habr_python'])
async def unsubscribe_user(message: types.Message) -> None:
    '''Функция отвечающая за отписку юзера на расслыку habr python'''
    user_id = str(message.from_user.id)
    try:
        if not database_habr_python.subsribe_exists(user_id):
            '''Если юзера нет в БД добавдяем его с неактивной подпиской'''
            database_habr_python.add_subscriber(user_id, False)
            await  message.answer(text_bot.UNSUBSCRIBE)

        else:
            '''иначе присваем юзеру статус неподписчика'''
            database_habr_python.update_subscriber(user_id, False)
            await message.answer(text_bot.UNSUBSCRIBE)

    except:
        raise exceptions.ErrorConnectToDB(await message.answer('Произошла ошибка подключения к базе данных'))


@dp.message_handler(commands=['subscribe_habr_bigdata'])
async def subscribe_user(message: types.Message) -> None:
    '''Функция отвечающая за подписку юзера на habr big data'''
    user_id = str(message.from_user.id)
    try:
        if not database_habr_big_data.subsribe_exists(user_id):
            '''Если юзера нет в БД добавдяем его с активной подпиской'''
            database_habr_big_data.add_subscriber(user_id, True)
            await  message.answer(text_bot.SUBSCRIBE_NEW)

        else:
            '''иначе присваем юзеру статус подписчика'''
            database_habr_big_data.update_subscriber(user_id, True)
            await message.answer(text_bot.SUBSCRIBE_OLD)

    except:
        raise exceptions.ErrorConnectToDB(await message.answer('Произошла ошибка подключения к базе данных'))


@dp.message_handler(commands=['unsubscribe_habr_bigdata'])
async def unsubscribe_user(message: types.Message) -> None:
    '''Функция отвечающая за отписку юзера на рассылку habr big data'''
    user_id = str(message.from_user.id)
    try:
        if not database_habr_big_data.subsribe_exists(user_id):
            '''Если юзера нет в БД добавдяем его с неактивной подпиской'''
            database_habr_big_data.add_subscriber(user_id, False)
            await  message.answer(text_bot.UNSUBSCRIBE)

        else:
            '''иначе присваем юзеру статус неподписчика'''
            database_habr_big_data.update_subscriber(user_id, False)
            await message.answer(text_bot.UNSUBSCRIBE)

    except:
        raise exceptions.ErrorConnectToDB(await message.answer('Произошла ошибка подключения к базе данных'))


@dp.message_handler(commands=['subscribe_tproger_python'])
async def subscribe_user(message: types.Message) -> None:
    '''Функция отвечающая за подписку юзера на рассылку stopgame'''
    user_id = str(message.from_user.id)
    try:
        if not database_tproger.subsribe_exists(user_id):
            '''Если юзера нет в БД добавдяем его с активной подпиской'''
            database_tproger.add_subscriber(user_id, True)
            await  message.answer(text_bot.SUBSCRIBE_NEW)

        else:
            '''иначе присваем юзеру статус подписчика'''
            database_tproger.update_subscriber(user_id, True)
            await message.answer(text_bot.SUBSCRIBE_OLD)

    except:
        raise exceptions.ErrorConnectToDB(await message.answer('Произошла ошибка подключения к базе данных'))


@dp.message_handler(commands=['unsubscribe_tproger_python'])
async def unsubscribe_user(message: types.Message) -> None:
    '''Функция отвечающая за отписку юзера на рассылку stopgame'''
    user_id = str(message.from_user.id)
    try:
        if not database_tproger.subsribe_exists(user_id):
            '''Если юзера нет в БД добавдяем его с неактивной подпиской'''
            database_tproger.add_subscriber(user_id, False)
            await  message.answer(text_bot.UNSUBSCRIBE)

        else:
            '''иначе присваем юзеру статус неподписчика'''
            database_tproger.update_subscriber(user_id, False)
            await message.answer(text_bot.UNSUBSCRIBE)

    except:
        raise exceptions.ErrorConnectToDB(await message.answer('Произошла ошибка подключения к базе данных'))


# асинхронная функция
async def main_malling_stop_game(time_wait: int) -> None:
    while True:
        await asyncio.sleep(time_wait)
        try:
            parser_stop_game.clear()  # очищаем список с ссылками
            new_games = parser_stop_game.new_game_href()
            if new_games:  # если появились новые обзоры на сайте
                new_games.reverse()
                for game in new_games:
                    info = parser_stop_game.parse_game_info(game)  # парсим данные игры
                    subsciptions = database_stopgame.get_subscriptions()  # получаем текущих подписчиков
                    parser_stop_game.download_image(info.poster)
                    with open('img_stop_game.jpg', 'rb') as photo:
                        for i in subsciptions:
                            await bot.send_photo(  # отправляем подписчикам инфу об игре
                                i[1],
                                photo,
                                caption=info.title + "\n" + "Оценка: " + info.score + "\n" + info.text + "\n\n" + info.href,
                                disable_notification=True
                            )
                            parser_stop_game.update_last_key(
                                parser_stop_game.parse_href(info.href))  # изменяем ключ игры

        except:
            subsciptions = database_habr_big_data.get_subscriptions()
            for i in subsciptions:
                await bot.send_message(
                    i[1],
                    str('Произошла ошибка парсера stopgame')
                )
            raise exceptions.ErrorParserStopgame('Произошла ошибка парсера stopgame')


async def main_malling_crackwatch(time_wait: int) -> None:
    while True:
        await asyncio.sleep(time_wait)
        try:
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

        except:
            subsciptions = database_habr_big_data.get_subscriptions()
            for i in subsciptions:
                await bot.send_message(
                    i[1],
                    str('Произошла ошибка парсера crackwatch')
                )
            raise exceptions.ErrorParserCrackWatch('Произошла ошибка парсера crackwatch')


async def mail_malling_habr_python(time_wait: int) -> None:
    while True:
        await asyncio.sleep(time_wait)
        try:
            res = parser_habr_python.parsing_block()
            subsciptions = database_habr_python.get_subscriptions()
            if res:
                for i in subsciptions:
                    await bot.send_message(
                        i[1],
                        str('Название: ' + res.title + '\n' + 'Тэги: ' + res.tags + '\n\n' + res.text + '\n' + res.href)
                    )
                parser_habr_python.update_last_key(res.key)
                parser_habr_python.clear()

        except:
            subsciptions = database_habr_big_data.get_subscriptions()
            for i in subsciptions:
                await bot.send_message(
                    i[1],
                    str('Произошла ошибка парсера habr')
                )
            raise exceptions.ErrorParserStopgame('Произошла ошибка парсера habr')


async def mail_malling_habr_big_data(time_wait: int) -> None:
    while True:
        await asyncio.sleep(time_wait)
        try:
            res = parser_habr_big_data.parsing_block()
            subsciptions = database_habr_big_data.get_subscriptions()
            if res:
                for i in subsciptions:
                    await bot.send_message(
                        i[1],
                        str('Название: ' + res.title + '\n' + 'Тэги: ' + res.tags + '\n\n' + res.text + '\n' + res.href)
                    )
                parser_habr_big_data.update_last_key(res.key)
                parser_habr_big_data.clear()

        except:
            subsciptions = database_habr_big_data.get_subscriptions()
            for i in subsciptions:
                await bot.send_message(
                    i[1],
                    str('Произошла ошибка парсера habr')
                )
            raise exceptions.ErrorParserStopgame('Произошла ошибка парсера habr')


async def mail_malling_tproger_python(time_wait: int) -> None:
    while True:
        await asyncio.sleep(time_wait)
        try:
            res = parser_tproger.parsing()
            print(res)
            subsciptions = database_habr_big_data.get_subscriptions()
            if res:
                for i in subsciptions:
                    await bot.send_message(
                        i[1],
                        str('Название: ' + res.title + '\n\n' + res.text + '\n' + res.href)
                    )
                parser_tproger.update_last_key(res.key)

        except:
            subsciptions = database_habr_big_data.get_subscriptions()
            for i in subsciptions:
                await bot.send_message(
                    i[1],
                    str('Произошла ошибка парсера tproger')
                )
            raise exceptions.ErrorParserTproger('Произошла ошибка парсера tproger')


if __name__ == '__main__':
    database_stopgame.check_database()  # проверяем существует ли БД
    dp.loop.create_task(main_malling_stop_game(30))  # запускаем асинхронные функции
    dp.loop.create_task(main_malling_crackwatch(30))
    dp.loop.create_task(mail_malling_habr_big_data(30))
    dp.loop.create_task(mail_malling_habr_python(30))
    dp.loop.create_task(mail_malling_tproger_python(30))
    executor.start_polling(dp, skip_updates=True)  # запускаем бота с игнором ошибок
