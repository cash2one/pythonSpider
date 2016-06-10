#-*- coding:utf-8 -*-

import requests
from HTMLParser import HTMLParser

class MyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'img' and self.getattrs(attrs, 'class') == 'verifyCode':
            verifyimg = self.getattrs(attrs, 'src')
            verifyurl = 'http://passport.jikexueyuan.com' + verifyimg
            print verifyurl

    def handle_data(self, data):
        print data

    def handle_startendtag(self, tag, attrs):
        print tag
        for attr in attrs:
            print 'attrs    ', attr

    def getattrs(self, attrs, attrname):
        for attr in attrs:
            if attr[0] == attrname:
                return attr[1]
        return None

# url = 'http://passport.jikexueyuan.com/sso/login'
# r = requests.get(url)
# html = r.content
mp = MyParser()
# mp.feed(html)
mp.feed('<button type="button" id="login" class="passport-btn passport-btn-def xl w-full" tabindex="4" jktag="0001|0.1|91038" href="javascript:;"/>fff</button>')