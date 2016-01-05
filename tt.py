#-*- coding:utf-8 -*-
import re
import urllib
import requests


def get_picurl(pic_content):
    picurl = []
    domain = "http://www.tuigirl.com"
    
    pattern = re.compile(r'src="(.*?)"')
    match = pattern.findall(pic_content)
    
    for pic in match:
        purl = domain + pic
        picurl.append(purl)
        le = len(picurl)
    else:
        return picurl

def download_pic(url):
    n = 0
    for i in url:
        img = requests.get(i).content
        open('img/' + str(n)+'.jpg', 'wb').write(img)
        n += 1
    else:
        print "Done!"
    

con = urllib.urlopen('tt.html')
html = con.read()
picurl = get_picurl(html)
download_pic(picurl)