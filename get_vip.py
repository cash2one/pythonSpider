#coding:utf-8
import re
import requests

import sys
reload(sys)
sys.setdefaultencoding('utf8')

url = 'http://www.ffaner.com'
source_html = requests.get(url).text
the_new = source_html.find(r'最新发布')

def get_vip(keyword, tag):
    link = get_link(keyword, tag)
    vip = get_account(link)
    return vip

def get_link(k, t):        
    paltform = source_html.find(k, t)
    a_link_start = source_html.find(r'http', paltform)
    a_link_end = source_html.find(r'"', a_link_start)
    link = source_html[a_link_start : a_link_end]
    return link

def get_account(l):
    link_html = requests.get(l).text
    content = link_html.find(r'class="article-content"')
    account_start = link_html.find(r'会员帐号：', content)
    account_end = link_html.find(r'&nbsp;', account_start)
    account = link_html[account_start : account_end]
    account = re.sub('<.*>', ' ', account)
    return account
    
keyword = raw_input(r"你想要哪个网站的VIP？[优酷/爱奇艺/乐视/迅雷]: ")
if not (keyword in ['优酷', '爱奇艺', '乐视', '迅雷']):
    print '只能是以上四个网站之一哦'
    keyword = raw_input(r"请重新输入网站名称: ")
test = get_vip(keyword, the_new)
print test
