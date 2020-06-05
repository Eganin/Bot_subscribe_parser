import requests
from bs4 import BeautifulSoup as bs4
import os.path
from collections import namedtuple
import lxml.html
from lxml import etree


class Habr(object):
    def __init__(self, flag: str = 'python', file_save: str = 'last_post_habr_python.txt') -> None:
        self.base_url_python = 'https://habr.com/ru/search/?target_type=posts'

        self.base_url_bigdata = 'https://habr.com/ru/search/?target_type=posts'

        self.params_python = {'q': 'python',
                              'order_by': 'date'}

        self.params_bigdata = {'q': 'big data',
                               'order_by': 'date'}

        self.flag = flag

        self.soup = bs4(self.get_page(), 'lxml')

        self.file_save = file_save

        self.tags = []

        self.text = []

        self.list_post = []

        self.img = []

        self.post = namedtuple('post', ['title', 'href', 'tags', 'text', 'key'])

        if os.path.exists(self.file_save):
            self.lastpost = open(self.file_save).read()

        else:
            '''Создание файла и запись в него ключа последней игры'''
            with open(file_save, 'w') as file:
                self.lastpost = self.get_last_post()
                file.write(self.lastpost)

    def get_page(self) -> str:
        if self.flag == 'python':
            r = requests.get(url=self.base_url_python, params=self.params_python)

        else:
            r = requests.get(url=self.base_url_bigdata, params=self.params_bigdata)
            print(r.url)

        return r.text

    def parsing_block(self) -> list or bool:
        block_parse = self.soup.select('article', attrs={'class': 'post.post_preview',
                                                         'lang': 'ru'})
        id = str(
            self.soup.select('li', attrs={'class': 'content-list__item.content-list__item_post.shortcuts_item.focus'})[
                10]['id'])
        for i in block_parse:
            href = i.find('a', attrs={'class': 'post__title_link'})['href'].strip()
            key = self.parse_href(href)
            if int(key) > int(self.lastpost) and int(key) != int(self.lastpost):
                title = i.find('a', attrs={'class': 'post__title_link'}).text.strip()
                tags = i.select('li', attrs={'class': 'inline-list__item.inline-list__item_hub'})

                '''Парсинг с помощью lxml т.к bs4 не видит текст'''
                tree = lxml.html.document_fromstring(self.get_page())
                text_post_lxml = tree.xpath(f'//*[@id="{id}"]/article/div/div/text()')
                for tag in tags:
                    self.tags.append(tag.text.strip())
                self.list_post.append(self.post(
                    title=title,
                    href=href,
                    tags=self.parse_tags(self.tags[:-4]),
                    text=self.parse_text(text_post_lxml),
                    key=key
                ))
                self.clear_closing()

            else:
                pass

        if self.list_post:
            return self.list_post[0]

        else:
            return False

    def update_last_key(self, result: str) -> str:
        '''обновление кдюча на последнюю вышедшую игру'''
        self.lastkey = result
        with open(self.file_save, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(result)
            f.truncate()

        return result

    def get_last_post(self) -> str:
        block_parse = self.soup.select('article', attrs={'class': 'post.post_preview',
                                                         'lang': 'ru'})
        for i in block_parse:
            href = self.parse_href(i.find('a', attrs={'class': 'post__title_link'})['href'])
            return href

    def parse_href(self, href: str) -> str:
        return href.split('/')[-2]

    def parse_text(self, text: list) -> str:
        for i in text:
            self.text.append(i.strip())

        return ' '.join(self.text)

    def parse_tags(self, tags: list) -> str:
        return ' '.join(tags)

    def clear_closing(self) -> None:
        self.tags[:] = []
        self.text[:] = []

    def clear(self) -> None:
        self.list_post[:] = []


clf = Habr(flag='bigdata', file_save='last_post_habr_bigdata.txt')
res = clf.parsing_block()
if res:
    print(res)
    clf.update_last_key(res.key)
    clf.clear()

else:
    print('end')