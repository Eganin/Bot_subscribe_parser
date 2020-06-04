import requests
import json
from collections import namedtuple
import os.path


class CrackWatch(object):
    def __init__(self, file_save: str = 'last_key_crackwatch.txt'):
        self.base_url = 'https://api.crackwatch.com/api/games'

        self.games_info = namedtuple('game',
                                     ['title', 'protections', 'groups', 'releaseDate', 'image', 'crackDate', 'href',
                                      'key'])
        'словарь с параметрами для запроса'
        self.get_crackgame = {'page': 0,
                              'is_released': 'true',
                              'is_cracked': 'true',
                              'sort_by': 'release_date'}

        self.file_save = file_save

        self.game = []

        if os.path.exists(self.file_save):
            self.last_name = open(file_save, 'r').read()
        else:
            '''Создание файла и запись в него ключа последней игры'''
            with open(file_save, 'w') as file:
                self.last_name = self.last_game()
                file.write(self.last_name)

    def get_game_json(self, params: dict) -> str:
        r = requests.get(self.base_url, params=params)
        return json.loads(r.text)

    def href_parse(self, href: str) -> str:
        return str(href)[28:]

    def parse_answer_api(self, info) -> namedtuple:
        return self.games_info(
            title=str(info['title']),
            protections=str(*info['protections']),
            groups=str(*info['groups']),
            releaseDate=str(info['releaseDate']),
            image=str(info['image']),
            crackDate=str(info['crackDate']),
            href=str(info['url']),
            key=self.href_parse(info['url'])
        )

    def new_game(self) -> namedtuple or bool:
        self.clear()
        while True:
            try:
                res_api = self.get_game_json(self.get_crackgame)
                print('accept')
                for i in res_api:
                    answer = self.parse_answer_api(i)
                    if answer.key != self.last_name:
                        self.update_name(answer.key)
                        return answer

                    else:
                        return False
            except:
                print('error')
                pass

    def last_game(self) -> namedtuple:
        while True:
            try:
                res_api = self.get_game_json(self.get_crackgame)
                for i in res_api:
                    answer = self.parse_answer_api(i)
                    self.game.append(answer)

                return self.game[0]

            except:
                pass

    def update_name(self, last_name: str) -> str:
        self.last_name = last_name
        with open(self.file_save, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(last_name)
            f.truncate()

        return last_name

    def download_image(self, img: str) -> None:
        '''Загрузка изображения'''
        p = requests.get(img)
        out = open("img_crackwatch.jpg", "wb")
        out.write(p.content)
        out.close()

    def clear(self):
        self.game[:] = []
