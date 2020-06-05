import sqlite3
from typing import List, Tuple
from exceptions import ErrorConnectDatabase
import os.path


class SQLither(object):
    '''Класс отвечающий за работу с БД'''

    def __init__(self, database: str = 'datasql', flag: str = 'subscriptions_stopgame') -> None:
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.database = flag

    def get_subscriptions(self, status: bool = True) -> List[Tuple[int, str, int]]:
        '''Получение все подписчиков бота'''
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM {self.database} WHERE status = ?", (status,)).fetchall()

    def subsribe_exists(self, user_id: str) -> bool:
        '''Проверка на наличие юзера в БД'''
        with self.connection:
            availability_user = self.connection.execute(f'SELECT * FROM {self.database} WHERE user_id = ?',
                                                        (user_id,)).fetchall()

            return bool(len(availability_user))

    def add_subscriber(self, user_id: str, status: bool = True) -> List[None]:
        '''Добавление нового подписчика в БД'''
        with self.connection:
            return self.cursor.execute(f'INSERT INTO {self.database} (user_id , status) VALUES (? , ?)',
                                       (user_id, status,)).fetchall()

    def update_subscriber(self, user_id: str, status: bool = True) -> List[None]:
        '''Обновление статуса подписки , для юзеров которые уже есть в БД'''
        with self.connection:
            return self.cursor.execute(f'UPDATE {self.database}  SET status = ? WHERE user_id = ?',
                                       (status, user_id,)).fetchall()

    def init_database(self):  # or os.system('sqlite3 db < database.sql')
        '''Инициализация БД'''
        with open("database.sql", "r") as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.connection.commit()

    def check_database(self):
        '''Проверка БД , если ее нет инициализирует'''
        if os.path.exists('datasql'):
            pass

        else:
            self.init_database()

    def close(self):
        '''Закрытие соединения с БД'''
        with self.connection:
            self.connection.close()

    def truncate(self):
        '''очистка таблмцы в крайнем случае'''
        with self.connection:
            self.cursor.execute('DELETE FROM subscriptions_crackwatch')
            self.cursor.execute('DELETE FROM subscriptions_stopgame')


