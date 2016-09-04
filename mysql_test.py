#!/usr/bin/env python3

import pymysql

conn = pymysql.connect(host="localhost", user="root", passwd=None, db="test", charset="utf8")
cur = conn.cursor()
sql = "select * from jb51_books"
cur.execute(sql)
print(cur.fetchall())
cur.connection.commit()
cur.close()
conn.close()
