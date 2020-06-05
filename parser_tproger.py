import requests
from bs4 import BeautifulSoup as bs4
import os.path
from collections import namedtuple
import lxml.html
from lxml import etree


class Tproger(object):
    def __init__(self, file_save: str = 'last_key_tpoger.txt') -> None:
        self.base_url = 'https://tproger.ru/tag/python/'

        self.soup = bs4(self.get_page(), 'lxml')

        self.cnt = -1

        self.post_info = namedtuple('post', ['href', 'title', 'text', 'key'])

        self.file_save = file_save

        if os.path.exists(self.file_save):
            self.lastpost = open(self.file_save).read()

        else:
            '''Создание файла и запись в него ключа последней игры'''
            with open(file_save, 'w') as file:
                self.lastpost = self.get_last_post()
                file.write(self.lastpost)

    def get_page(self) -> str:
        r = requests.get(self.base_url)
        return r.text

    def parsing(self) -> namedtuple or bool:
        self.clear()
        block = self.soup.select('a.article-link')
        for i in block:
            self.cnt += 1
            href = i['href']
            id = self.soup.select('article', attrs={
                'class': 'box.item.post-129792.post.type-post.status-publish.format-standard.has-post-thumbnail.hentry.category-articles.tag-python.tag-db.tag-tools.post-icon'})[
                0]['id']
            tree = lxml.html.document_fromstring(self.get_page())
            title = tree.xpath(f'//*[@id="{id}"]/div[1]/div[1]/h2/text()')
            text = tree.xpath(f'//*[@id="{id}"]/div[1]/div[2]/div/p/text()')
            if self.lastpost != id:
                return self.post_info(
                    href=href,
                    title=self.parse_title_text(title),
                    text=self.parse_title_text(text),
                    key=id
                )

            else:
                return False

    def get_last_post(self) -> str:
        block = self.soup.select('a.article-link')
        for i in block:
            self.cnt += 1
            id = self.soup.select('article', attrs={
                'class': 'box.item.post-129792.post.type-post.status-publish.format-standard.has-post-thumbnail.hentry.category-articles.tag-python.tag-db.tag-tools.post-icon'})[
                0]['id']

            return str(id)

    def update_last_key(self, result: str) -> str:
        '''обновление кдюча на последнюю вышедшую игру'''
        self.lastpost = result
        with open(self.file_save, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(result)
            f.truncate()

        return result

    def parse_title_text(self, result: list):
        return ' '.join(result)

    def clear(self):
        self.cnt = -1
