# -*- coding:utf8 -*-

import requests
import pymysql
from bs4 import BeautifulSoup as bs


class jb51_book(object):
    '''该类下使用4个方法
    1. 获取所有图书分类。返回分类名称和分类目录URL
    2. 根据返回的目录URL获取目录下所有图书链接URL
    3. 根据第2步返回的URL，获取图书标题和下载链接，下载链接取3个，并返回这4者
    4. 保存第3步返回和图书标题和下载链接到数据库中'''

    home_url = "http://www.jb51.net"
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2816.0 Safari/537.36'}

    def __init__(self, cur):
        self.cur = cur

    def get_catogory(self):
        catogory_info = dict()
        book_page = self.session.get("http://www.jb51.net/do/book_class.html", headers=self.headers)
        book_page_html = book_page.text.encode(book_page.encoding)
        # print(book_page_html)

        bsObj = bs(book_page_html, 'html.parser')
        catogorys = bsObj.findAll("dl", {"class": "fix"})
        for catogory in catogorys:
            for item in catogory.dt.next_siblings:
                if item.name == 'dd':
                    for i in item.findAll("a"):
                        url = i.attrs['href']
                        if url not in catogory_info['url']:
                            catogory_info['name'] = i.get_text()
                            catogory_info['url'] = url
        return catogory_info

    def get_book_url(self, catogory_name, catogory_url):
        pass

    def get_book_info(self, catogory_name, book_url):
        page = self.session.get(book_url)
        page_html = page.text.encode(page.encoding)

        bsObj = bs(page_html, 'html.parser')
        book_name = bsObj.find("h1", {"itemprop": "name"}).get_text()
        download_links = bsObj.find("ul", {"class": "ul_Address"}).findAll("a")
        i = 1
        download_link = []
        while i < 4:
            download_link.append(download_links[i].attrs['href'])
            i += 1
        sql = "INSERT INTO jb51_books (catogory, book_name, book_url, download_url1, download_url2, download_url3) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")" % \
              (catogory_name, book_name, book_url, download_link[0], download_link[1], download_link[2])
        self.cur.execute(sql)
        self.cur.connection.commit()
        self.cur.close()


if __name__ == '__main__':
    conn = pymysql.connect(host="localhost", user="root", passwd="root", db="test", charset="utf8")
    cur = conn.cursor()
    spider = jb51_book(cur)
    # spider.get_catogory()
    spider.get_book_info("PHP", "http://www.jb51.net/books/471440.html")
