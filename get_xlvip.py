import requests
import re

url = 'http://www.xlfans.com'
source = requests.get(url)
source_html = source.text

first_div = source_html.find(r'class="label label-important"')
h2 = source_html.find(r'<h2>', first_div)
a_link_start = source_html.find(r'http', h2)
a_link_end = source_html.find(r'"', a_link_start)
link = source_html[a_link_start : a_link_end]
#print link

vip_source_html = requests.get(link).text
vip_start = vip_source_html.find(r'迅雷粉独家迅雷会员')
vip_end = vip_source_html.find(r'转载请注明')
vip = vip_source_html[vip_start : vip_end]
vip = re.sub('<.*>', ' ', vip)
print vip
