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
    单线程版
    本程序用于提取豆瓣中所有包含“广州”的小组
    提取其名称、成员数量、链接
    ''' 

    def __init__(self, conn, cur, session):

        self.session = session 

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

        groups_url = []
        for i in range(0, 2001, 20):
            url = r"https://www.douban.com/group/search?start=%s&cat=1019&sort=relevance&q=广州" % i
            groups_url.append(url)

        return groups_url

    def get_group_info(self, page_url):
        '''
        解析页面，得到组名、链接地址、成员数量
        并打印出来
        '''

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
            print("%s\n%s\n%s\n***************************************" % (group_name, group_url, group_member))
            #self.insert_db(group_name, group_url, group_member)

    def insert_db(self, name, url, member):
        print('插入数据库')
        try:
            sql_insert = "INSERT INTO douban_gz_group (group_name, group_url, group_member) values ('%s', '%s', '%s')" % (name, url, member)
            self.cur.execute(sql_insert)
            self.conn.commit()
        except Exception:
            self.conn.rollback()

def login_douban(username, password):
    '''
    本函数用于登录豆瓣，并返回session共其它函数使用
    因为经测试，如果不登录，则只能查看搜索结果前10页的信息
    登录后才可能查看更多页面
    '''
    
    session = requests.Session()
    login_url = "https://accounts.douban.com/login"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
    }

    preload = {
        'source': 'None',
        'redir': 'https://www.douban.com/people/92549523/',
        'form_email': username,
        'form_password': password,
        'remember': 'on',
        'login': u'登录'
        }
    
    r = session.get(login_url)
    html = r.content
    bsObj = bs(html, 'lxml')

    # 检测是否需要验证码
    # 如果需要，则提取验证码图片，人工打码
    try:
        cap = bsObj.find('img', {'id': 'captcha_image'})
        captcha_url = cap.attrs['src']
        captcha = input('Please input the captcha code %s :' % captcha_url)
        preload['captcha-solution'] = captcha

        cap_id = bsObj.find('input', {'name': 'captcha-id'})
        captcha_id = cap_id.attrs["value"]
        preload['captcha-id'] = captcha_id
    except Exception:
        pass


    session.post(login_url, headers=headers, data=preload)
    return session

if __name__ == '__main__':

    # 输入豆瓣的账号密码以登录豆瓣并获取全局session
    session = login_douban('username', 'passowrd')

    # 连接数据库并获取游标
    conn = pymysql.connect(host='localhost', user='root', passwd=None, db='test', charset='utf8')
    cur = conn.cursor()
    
    # 创建实例，并获取所有小组分页
    gz_db = Db_gz_group(conn, cur, session)
    pages = gz_db.get_all_page()

    for page in pages:
        gz_db.get_group_info(page)

    # 关闭数据库连接
    cur.close()
    conn.close()

    print("Finish All")
