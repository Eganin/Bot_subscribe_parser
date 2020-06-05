import os.path
import requests
from bs4 import BeautifulSoup as bs4
from collections import namedtuple
from typing import List, NamedTuple
import re


class StopGame(object):
    '''Класс отвечающий за парснг сайта stopgame'''

    def __init__(self, file_save: str = 'last_key_parser.txt') -> None:
        self.base_url = 'https://stopgame.ru/review/new/'
        self.info = namedtuple('game', ['poster', 'text', 'score', 'title', 'href'])
        self.new_url = 'https://stopgame.ru'
        self.href_game = []
        self.file_save = file_save
        if os.path.exists(self.file_save):
            self.lastkey = open(file_save, 'r').read()

        else:
            '''Создание файла и запись в него ключа последней игры'''
            with open(file_save, 'w') as file:
                self.lastkey = self.parse_href(self.last_href())
                file.write(self.lastkey)

    def new_game_href(self) -> List[str]:
        '''функция находит новые выпущенные статьи'''
        r = requests.get(self.base_url)
        soup = bs4(r.content, 'lxml')
        block_href = soup.select('div.item.article-summary.article-summary-card')
        for i in block_href:
            try:
                href = self.new_url + str(i.find('a', attrs={'href': True})['href'])
                href_parse = self.parse_href(href)

                if int(href_parse) > int(self.lastkey) and int(href_parse) != int(self.lastkey):  # сверка с ключом
                    self.href_game.append(href)

            except:
                href = ''

        return self.href_game

    def parse_game_info(self, url: str) -> NamedTuple:
        '''парсинг данных игры'''
        r = requests.get(url)
        soup = bs4(r.content, 'lxml')
        try:
            poster = re.match(r'background-image:\s*url\((.+?)\)', soup.select('.image-game-logo > .image')[0]['style'])

        except:
            poster = ''

        try:
            excpert_text = soup.select('.article.article-show')[0].text[0:400] + '...'

        except:
            excpert_text = ''

        try:
            score = self.sum_score(soup.select('.game-stopgame-score > .score')[0]['class'][1])

        except:
            score = ''

        block_game = soup.select('div.game-details')
        for info in block_game:
            try:
                title = info.find('h1', attrs={'class': 'article-title'}).text

            except:
                title = ''

            try:
                href = url

            except:
                href = ''

            return self.info(poster=poster.group(1),
                             text=excpert_text,
                             score=score,
                             title=title,
                             href=href)

    def sum_score(self, score):
        '''преобразователь в оценку'''
        if score == 'score-1':
            return "Мусор"
        elif score == 'score-2':
            return "Проходняк"
        elif score == 'score-3':
            return "Похвально👍👍👍👍"
        elif score == 'score-4':
            return "Изумительно "

    def update_last_key(self, result: str) -> str:
        '''обновление кдюча на последнюю вышедшую игру'''
        self.lastkey = result
        with open(self.file_save, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(result)
            f.truncate()

        return result

    def last_href(self) -> str:
        '''Врзвращает ссылку последней ишоы на сайте'''
        r = requests.get(self.base_url)
        soup = bs4(r.content, 'lxml')
        block_href = soup.select('div.item.article-summary.article-summary-card')
        for i in block_href:
            href = i.find('a')['href']
            return self.new_url + str(href)

    def download_image(self, img: str) -> None:
        '''Загрузка изображения'''
        p = requests.get(img)
        out = open("img_stop_game.jpg", "wb")
        out.write(p.content)
        out.close()

    def parse_href(self, href: str) -> str:
        '''Парсинг ссылки для выявления ключа'''
        result = href[25:]
        key = result.split('/')[0]
        return str(key)

    def clear(self):
        '''после парсинга очищается спислк с ссылками на игру'''
        self.href_game[:] = []
