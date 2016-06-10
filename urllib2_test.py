#!D:/Python27/Python27.exe
#-*- coding:utf8 -*-

import urllib2

login = 'admin'
passwd = 'x45668668'
url = 'http://www.xjr7670.com'

def handler_version(url):
	from urlparse import urlparse
	hdlr = urllib2.HTTPBasicAuthHandler()
	hdlr.add_password('Archives', urlparse(url)[1], login, passwd)
	opener = urllib2.build_opener(hdlr)
	urllib2.install_opener(opener)
	return url

def request_version(url):
	from base64 import encodestring
	req = urllib2.Request(url)
	b64str = encodestring('%s:%s' % (login, passwd))[:-1]
	req.add_header("Authorization", "Basic %s" % b64str)
	return req

for funcType in ('handler', 'request'):
	print '*** Using %s:' % funcType.upper()
	url = eval('%s_version')(URL)
	f = urllib2.urlopen(url)
	print f.readline()
	f.close