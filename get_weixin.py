#-*- encoding:utf-8 -*-

import requests
import json

url = 'http://v.juhe.cn/weixin/query'
params = {
    "pno" : "",
    "ps" : "",
    "key" : "5076be8b86c2166fd210e88cfe13f544",
    "dtype" : "",
    }

r = requests.get(url, params=params)
result = json.loads(r.text)
print('标题：', result["result"]["list"][0]["title"])
print('URL：', result["result"]["list"][0]["url"])

for i in range(0, 10):
    print(i)
	print(i=)
	
