#!/usr/bin/env python3
# -*- coding:utf8 -*-

import time
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

    def get_catogory(self, class_url):
        # 本函数用于获取所有图书目录
        # 最后以列表形式返回图书目录名称和URL

        catogory_info = []
        book_page = self.session.get(class_url, headers=self.headers, timeout=10)
        book_page_html = book_page.text.encode(book_page.encoding)
        # print(book_page_html)

        bsObj = bs(book_page_html, 'lxml')
        catogorys = bsObj.findAll("dl", {"class": "fix"})
        for catogory in catogorys:
            for item in catogory.dt.next_siblings:
                if item.name == 'dd':
                    for i in item.findAll("a"):
                        url = i.attrs['href']
                        name = i.get_text()
                        catogory_info.append({"name": name, "url": url})
        return catogory_info

    def get_catogory_all_page(self, catogory_url):
        # 得到该分类下有多少个页面


        # 先获取分类URL的前缀，以方便翻页
        pre_url = catogory_url[:-6]

        r = self.session.get(self.home_url + catogory_url, headers=self.headers, timeout=10)
        html = r.content
        bsObj = bs(html, 'lxml')
        a_tag =  bsObj.find("div", {"class": "plist"}).findAll("a")
        last_page_url = a_tag[-1].attrs['href']
        last_page_num = int(last_page_url[last_page_url.find("_")+1: last_page_url.find(".html")])

        sum_page = last_page_num + 1
        catogory_all_url = set()

        for i in range(1, sum_page):
            catogory_all_url.add(pre_url + str(i) + '.html')

        return catogory_all_url

    def get_book_url(self, catogory_all_url):
        # 根据传进来的分类目录URL集，获取其中的所有图书链接

        book_urls = set()
        for url in catogory_all_url:
            try:
                r = self.session.get(self.home_url + url, headers=self.headers, timeout=10)
            except Exception:
                print("%s 页面图书链接提取超时，继续抓取下一页" % url)
                continue
            else:
                html = r.content
                bsObj = bs(html, 'lxml')
                book_list = bsObj.findAll("a", {"class": "tit"})
                for book in book_list:
                    book_url = book.attrs['href']
                    if book_url not in book_urls:
                        book_urls.add(book_url)

        return book_urls

    def get_book_info(self, catogory_name, book_url):
        # 本函数根据传进来的图书链接，获取图书相关信息
        # 包括书名、下载链接
        # 最后把图书所属分类、书名、页面URL、下载链接1、下载链接2、下载链接3插入到数据库中

        print("获取图书信息...")
        page = self.session.get(self.home_url + book_url, timeout=10)
        
        page_html = page.content

        bsObj = bs(page_html, 'lxml')
        book_name = bsObj.find("h1", {"itemprop": "name"}).get_text()
        download_links = bsObj.find("ul", {"class": "ul_Address"}).findAll("a")
        print("图名为：%s \t 链接： %s" % (book_name, book_url))
        download_link = [None]*3
        links_length = len(download_links)
        if links_length >=4:
            i = 1
            while i < 4:
                download_link[i-1] = download_links[i].attrs['href']
                i += 1
        else:
            for i in range(0, links_length):
                download_link[i] = download_links[i].attrs['href']
            

        sql = "INSERT INTO jb51_books (catogory, book_name, book_url, download_url1, download_url2, download_url3) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")" % (catogory_name, book_name, book_url, download_link[0], download_link[1], download_link[2])
        print("正在插入数据库...")
        self.cur.execute(sql)
        self.cur.connection.commit()


if __name__ == '__main__':
    f = open('time.txt', 'a')
    f.write(time.ctime())
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="test", charset="utf8")
    cur = conn.cursor()
    spider = jb51_book(cur)
    catogorys = spider.get_catogory("http://www.jb51.net/do/book_class.html")

    for catogory in catogorys:
        catogory_name = catogory['name']
        catogory_url = catogory['url']

        print("正在处理目录：", catogory_name)
        
        try:
            cagotory_all_page = spider.get_catogory_all_page(catogory_url)
            print("已获取该目录下所有页面链接，开始抓取这些页面上的图书链接")
            
            book_urls = spider.get_book_url(cagotory_all_page)
            
            print("图书链接抓取完毕，开始提取图书信息并插入数据库")

            for book_url in book_urls:
                try:
                    spider.get_book_info(catogory_name, book_url)
                except Exception:
                    print("抓取超时，跳过，开始处理下一本书")
                    continue
                else:
                    time.sleep(5)
        except Exception:
            print("抓取超时，跳过，开始处理下一目录")
            continue

    cur.close()
    conn.close()
    f.write(time.ctime())
    f.close()
