import requests

url = 'http://weibo.cn'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '_T_WM=66e6770df4eaea4809431abf5805d475; ALF=1467979448; SUB=_2A256XGTlDeTxGedM7VQS9SzFzz-IHXVZvwytrDV6PUJbktBeLVOkkW0iOjUCNwAI3Z3RnJf7vKv1jUXZvg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhcybNwiDOTARDUySlQEOwz5JpX5o2p5NHD95Qpeoqce0-E1KB0Ws4Dqcj.i--RiKn7iKnpi--Ri-z0i-2Ei--ciK.Ri-8si--Ri-8Wi-z7; SUHB=0BLpJwseSbfsnS; SSOLoginState=1465390261; gsid_CTandWM=4uZ3CpOz5qdbESRsqSgVp5jr2fd',
    'Host': 'weibo.cn',
    'Pragma': 'no-cache',
    'Referer': 'http://login.sina.com.cn/sso/login.php?url=http%3A%2F%2Fweibo.cn%2F&_rand=1465390258.2503&gateway=1&service=sinawap&entry=sinawap&useticket=1&returntype=META&sudaref=&_client_version=0.6.22',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36'
}
r = requests.post(url, headers=headers)
fobj = open('weibo.cn.html', 'w')
fobj.write(r.content)