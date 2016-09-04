#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from wordpress_xmlrpc import Client
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts
from wordpress_xmlrpc.methods.posts import GetPosts
from wordpress_xmlrpc.methods.posts import NewPost

# 连接服务器
client = Client('http://wordpress.localhost/xmlrpc.php', 'admin', 'my_password')

# 获取发贴对象
post = WordPressPost()

# 设置文章标题
post.title = "My post from python"

# 添加文章内容
post.content = "This is a wonderful blog post about XML-RPC."
#post.id = client.call(NewPost(post))

# 设置文章分类和标签
post.terms_names = {
        'post_tag': ['test', 'python post'],
        'category': ['Tests']
        }

# 把状态设置为“发布“
post.post_status = 'publish'

# 发布文章
client.call(NewPost(post))

# 获取所有文章
articles = client.call(GetPosts())
# 返回的articles是个列表对象
for article in articles:
    # 调用每个文章对象的struct属性可以得到这个文章的结构，是一个字典
    print(article.struct['post_title'])
