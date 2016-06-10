#-*- coding:utf-8 -*-
import re

class get_attr(object):
    def __init__(self):
        self.url = []
        self.link_name = []

    def get_link(self, html):
        href = re.compile('href="(.*)"', re.I)
        self.url = href.findall(html)

    def get_linkto(self, html):
        linkto = re.compile('"\s?>(.*)</a>', re.I)
        self.link_name = linkto.findall(html)

def format(url, link_name):
    for u1, l1 in enumerate(link_name):
        print ' %d. [%s][%d]' % (u1+1, l1, u1+1)
 
    print '\n'

    for u2, l2 in enumerate(url):
        print '  [%d]: %s' % (u2+1, l2)

if __name__ == '__main__':
    r = open('link.html', 'r')
    html = r.read()
    r.close()
    ga = get_attr()
    ga.get_link(html)
    ga.get_linkto(html)
    url = ga.url
    link_name = ga.link_name
    format(url, link_name)