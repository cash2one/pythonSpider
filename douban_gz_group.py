#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup as bs

class db_gz_group(object):
    '''
    本程序用于提取豆瓣中所有包含“广州”的小组
    提取其名称、成员数量、链接
    ''' 

    def __init__(self):
        self.url = r"https://www.douban.com/group/search?cat=1019&q=广州"
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0",
                   "Host": "www.douban.com",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Accept-Language": "zh,zh-CN;q=0.8,en-US;q=0.5,en;q=0.3"}

        self.r = requests.get(self.url, headers=self.headers)
        self.html = self.r.content
        self.pat = re.compile('\d+')
        try:
            self.bsObj = bs(self.html, 'lxml')
        except:
            self.bsObj = bs(self.html, 'html.parser')

    def get_group_info(self):
        groups = self.bsObj.find("div", {"class": "groups"}).findAll("div", {"class": "result"})
        for group in groups:
            a_tag = group.find("a", {"class": "nbg"})
            group_name = a_tag.attrs['title']
            group_url = a_tag.attrs['href']
            group_info = group.find("div", {"class": "info"}).get_text()
            group_member = self.pat.search(group_info).group(0)
            print("组名：%s\n地址：%s\n成员数：%s" % (group_name, group_url, group_member))
            print("***********************************************************************************************")

if __name__ == '__main__':
    gz_db = db_gz_group()
    gz_db.get_group_info()
