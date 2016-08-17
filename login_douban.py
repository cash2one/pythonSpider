#!/usr/bin/python3
#-*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

class douban_crawler(object):
    def __init__(self, session):
        self.session = session

    def login_douban(self, username, password):
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

        # get captcha and captcha id
        try:
            cap = bsObj.find('img', {'id': 'captcha_image'})
            captcha_url = cap.attrs['src']
            captcha = input('Please input the captcha code %s :' % captcha_url)
            preload['captcha-solution'] = captcha

            cap_id = bsObj.find('input', {'name': 'captcha-id'})
            captcha_id = cap_id.attrs["value"]
            preload['captcha-id'] = captcha_id
        except:
            pass


        main_page = self.session.post(login_url, headers=headers, data=preload)
        print(main_page.text[:1000] + '\n Login successful!')
        return main_page
    
    def get_ck(self, main_page):
        html = main_page.text
        bsObj = BeautifulSoup(html, 'lxml')
        ck_tag = bsObj.find("input", {"name": "ck"})
        ck = ck_tag.attrs["value"]
        print(ck + '\tGet ck successful!')
        return ck

    def edit_signature(self, ck, signature):
        url = "https://www.douban.com/j/people/92549523/edit_signature"
        data = {"ck": ck, "signature": signature}
        change_signature = self.session.post(url, data=data)
        return change_signature.status_code

if __name__ == '__main__':
    session = requests.Session()
    login = douban_crawler(session)
    username = input("Please enter your douban account: ")
    password = input("Please enter your password: ")
    main_page  = login.login_douban(username, password)
    ck = login.get_ck(main_page)
    signature = input("What signature do you want? ")
    result = login.edit_signature(ck, signature)
    print(result)
