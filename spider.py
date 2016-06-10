#-*- coding:utf-8 -*-
import requests
import time
def crawler(keyword):
	res = requests.get('http://www.baidu.com/s?wd=' + keyword)
	html = res.text
	
	h3_begin = html.find(r'<h3')
	h3_end = html.find(r'</h3>', h3_begin)

	h3_content = html[h3_begin : h3_end]
	print h3_content

t0 = time.time()
crawler('php')
t = time.time() - t0
print t

















