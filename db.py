import sqlite3
from typing import List, Tuple


class SQLither(object):
    def __init__(self, database: str = 'db') -> None:
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status: bool = True) -> List[Tuple[int, str, int]]:
        '''Получение все подписчиков бота'''
        with self.connection:
            return self.cursor.execute("SELECT * FROM subscriptions WHERE status = ?", (status,)).fetchall()

    def subsribe_exists(self, user_id: str) -> bool:
        '''Проверка на наличие юзера в БД'''
        with self.connection:
            availability_user = self.connection.execute('SELECT * FROM subscriptions WHERE user_id = ?',
                                                        (user_id,)).fetchall()

            return bool(len(availability_user))

    def add_subscriber(self, user_id: str, status: bool = True) -> List[None]:
        '''Добавление нового подписчика в БД'''
        with self.connection:
            return self.cursor.execute('INSERT INTO subscriptions (user_id , status) VALUES (? , ?)',
                                       (user_id, status,)).fetchall()

    def update_subscriber(self, user_id: str, status: bool = True) -> List[None]:
        '''Обновление статуса подписки , для юзеров которые уже есть в БД'''
        with self.connection:
            return self.cursor.execute('UPDATE subscriptions  SET status = ? WHERE user_id = ?',
                                       (status, user_id,)).fetchall()

    def init_database(self):  # or os.system('sqlite3 db < database.sql')
        '''Инициализация БД'''
        with open("createdb.sql", "r") as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.connection.commit()

    def check_database(self):
        '''Проверка БД , если ее нет инициализирует'''
        self.cursor.execute("SELECT name FROM sqlite_master "
                            "WHERE type='table' AND name='subscriptions'")

        table_exists = self.cursor.fetchall()
        if table_exists:
            pass

        else:
            self.init_database()

    def close(self):
        '''Закрытие соединения с БД'''
        with self.connection:
            self.connection.close()

    def truncate(self):
        with self.connection:
            self.cursor.execute('DELETE FROM subscriptions')


