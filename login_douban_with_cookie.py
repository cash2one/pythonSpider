#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# 豆瓣不允许以cookie登录了，本程序无效
import requests
from bs4 import BeautifulSoup as bs

url = "https://www.douban.com/group/search?start=240&cat=1019&sort=relevance&q=%E5%B9%BF%E5%B7%9E"
cookies = '''ll="118281"; bid=fC3ti1k0ZFk; _pk_id.100001.8cb4=0fed7e48c0d92caf.1471346727.46.1473066784.1473062455.; push_noty_num=0; push_doumail_num=0; ap=1; __utma=30149280.220474596.1471346736.1473062436.1473065554.45; __utmz=30149280.1472558856.30.3.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=python%20class%20%E4%B8%8D%E5%B8%A6self%E7%9A%84%E6%96%B9%E6%B3%95; __utmv=30149280.9254; dbcl2="92549523:Uo1EfqkbdsY"; _vwo_uuid_v2=E7B7425228BAFC84B7FE49A817C7592D|883469d4b0eeb4271100aa42eb0259d9; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1473065552%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dgo0qDtIHEtAiGFuV0_4a7HvEs6wwFgW6bo1qONVXXhSLq2tmUsCRRmMKkSHXeXi1iII5NSyUw1Sky41cmbh2VK%26wd%3D%26eqid%3Da51c4af2000cc6080000000657b8fdbf%22%5D; ct=y; gr_user_id=209cd814-3c05-42c5-bbfd-7f78dabece3b; _ga=GA1.2.220474596.1471346736; ck=zceJ; __utmc=30149280; _pk_ses.100001.8cb4=*; __utmb=30149280.16.10.1473065554'''

headers = {'cookie': cookies}
r = requests.post(url, headers=headers)
html = r.text
print(html)
