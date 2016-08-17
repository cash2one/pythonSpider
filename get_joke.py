# -*- coding: utf-8 -*-
from urllib import request
import json
import pprint

url = 'http://apis.baidu.com/showapi_open_bus/showapi_joke/joke_text?page=1'


req = request.Request(url)

req.add_header("apikey", "457def328dc993292d61ab51edc7d3a1")

resp = request.urlopen(req)
content = resp.read()
if(content):
    #c = json.loads(content)
    pprint.pprint(content)
