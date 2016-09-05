#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import re
import threading
import requests
import pymysql
from time import sleep
from bs4 import BeautifulSoup as bs

class Db_gz_group(object):
    '''
    本程序用于提取豆瓣中所有包含“广州”的小组
    提取其名称、成员数量、链接
    ''' 

    def __init__(self, conn, cur):

        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0",
                        "Host": "www.douban.com",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "zh,zh-CN;q=0.8,en-US;q=0.5,en;q=0.3"}
        self.session =  requests.Session()
        self.session.headers.update(self.headers)

        # 编译两个正则表达式对象
        # 分别用于匹配组成员数量和去除组名称中的推荐星级
        self.member_pat = re.compile('\d+')
        self.name_pat = re.compile(r'（推荐.+）')

        self.conn = conn
        self.cur = cur

        
    def get_all_page(self):
        '''
        构造小组搜索结果页的URL地址
        结果数量与豆瓣结果显示的页数不一致
        当前观察到只有101页
        '''

        groups_url = set()
        for i in range(0, 2001, 20):
            url = r"https://www.douban.com/group/search?start=%s&cat=1019&sort=relevance&q=广州" % i
            groups_url.add(url)

        return groups_url

    def get_group_info(self, page_url, threadLock):
        '''
        解析页面，得到组名、链接地址、成员数量
        并打印出来
        '''

        threadLock = threadLock
        url = page_url
        print('正在处理：%s' % url)
        r = self.session.get(url)
        html = r.content
        try:
            bsObj = bs(html, 'lxml')
        except:
            bsObj = bs(html, 'html.parser')

        # 获取组div中的信息
        groups = bsObj.find("div", {"class": "groups"}).findAll("div", {"class": "result"})
        for group in groups:
            a_tag = group.find("a", {"class": "nbg"})
            
            # 获取组名并去除推荐星级信息
            group_name = a_tag.attrs['title']
            group_name = self.name_pat.sub('', group_name) 

            # 获取小组地址和成员数量
            group_url = a_tag.attrs['href']
            group_info = group.find("div", {"class": "info"}).get_text()
            group_member = self.member_pat.search(group_info).group(0)

            # 由于mysql是线程安全的，只允许单线程写入
            # 因此在进行写入操作时，要先获取线程锁，以防止多个线程同时对数据表进行写入
            threadLock.acquire()
            self.insert_db(group_name, group_url, group_member)
            # 写完之后，释放线程锁
            threadLock.release()

    def insert_db(self, name, url, member):
        try:
            sql_insert = "INSERT INTO douban_gz_group (group_name, group_url, group_member) values ('%s', '%s', '%s')" % (name, url, member)
            self.cur.execute(sql_insert)
            self.conn.commit()
        except Exception:
            self.conn.rollback()

if __name__ == '__main__':

    # 连接数据库并获取游标
    conn = pymysql.connect(host='localhost', user='root', passwd=None, db='test', charset='utf8')
    cur = conn.cursor()
    
    # 创建实例，并获取所有小组分页
    gz_db = Db_gz_group(conn, cur)
    pages = gz_db.get_all_page()

    threads = []

    # 设置线程锁
    threadLock = threading.Lock()

    # 添加线程
    for page in pages:
        t = threading.Thread(target=gz_db.get_group_info, args=(page, threadLock))
        threads.append(t)
    
    # 开始执行线程
    for thread in threads:
        thread.start()
        # 防止豆瓣反爬虫，每开始一个后，都先暂停5秒
        sleep(5)

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    # 关闭数据库连接
    cur.close()
    conn.close()

    print("Finish All")
