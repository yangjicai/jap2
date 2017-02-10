# coding:utf8
import pymysql
import methods

# Try to connect

try:
    conn = pymysql.connect('192.168.11.2','weixin','weixin','weixin',charset='utf8' )
except:
    print("I am unable to connect to the database.")

cur = conn.cursor()

try:
    cur.execute("""
 CREATE TABLE tangshilist(
 id MEDIUMINT NOT NULL AUTO_INCREMENT,
 category varchar(20),
 title varchar(50),
 author varchar(15),
 content varchar(350),
 PRIMARY KEY (id)
 );
     """)
except:
    print("I can't create table")

# try:
#     cur.execute("""
#  CREATE TABLE imglist(
#  id  int,
#  src VARCHAR(500)
#  );
#      """)
# except:
#     print ( "I can't create table")


# list = methods.getMsgList()
#
# query =  'INSERT INTO imglist (id, src) VALUES ({}, "{}");'
#
# i = 1
#
# for msg in list:
#     print(i)
#     data = (i , msg)
#     str = query.format(i,msg)
#     cur.execute(str.encode('utf-8'))
#     i = i + 1

cur.close()
conn.commit()
if conn is not None:
    conn.close()