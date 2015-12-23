import requests
import re

data = {'Host':'xlfans.com',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2540.0 Safari/537.36',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cookie':'__cfduid=dd06c3b83d9a84f0fa522699f8d646cea1445230668;Hm_lvt_8de0d99e331016cae1574e9062a24165=1448702361,1449564799,1450770098,1450847829;Hm_lpvt_8de0d99e331016cae1574e9062a24165=1450847829'}
url ='http://www.xlfans.com'
source = requests.post(url, data=data)
source_html = source.text

first_div = source_html.find(r'class="label label-important"')
h2 = source_html.find(r'<h2>', first_div)
a_link_start = source_html.find(r'http', h2)
a_link_end = source_html.find(r'"', a_link_start)
link = source_html[a_link_start : a_link_end]
#print link

vip_source_html = requests.get(link).text
vip_start = vip_source_html.find(r'一个月2元')
vip_end = vip_source_html.find(r'转载请注明')
vip = vip_source_html[vip_start+17 : vip_end]
vip = re.sub('<.*>', ' ', vip)
print vip
