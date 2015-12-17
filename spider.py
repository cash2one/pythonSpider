import requests
def crawler(url):
	res = requests.get(url)
	html = res.text
	
