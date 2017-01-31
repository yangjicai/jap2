#/usr/bin/python3
#coding=utf8

import os
import requests
import itchat
import time
import random
import re
from bs4 import BeautifulSoup

def getmsg():
    lilist = []
    strslist = []
    url = "http://www.v5jp.com/html/fuxi/fuxi001_"
    url_end = ".html"
    pageid = ["01","02","03","04","05"]

    for i in range(5):
        r = requests.get(url + pageid[i] + url_end)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text,"html.parser")

        page = soup.find("ul","fxxx")
        taglists = BeautifulSoup(str(page),"html.parser")
        xx = taglists.find_all("li")
        lilist.extend(xx)

    for li in lilist:
        strs = str(li)
        strs = re.sub(r'</?\w+[^>]*>','',strs)
        strslist.append(strs)

    return strslist
q = getmsg()


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    print(msg)
    print(msg['Text'])
    print(msg['FromUserName'])
    if str(msg['Text']) in [u'语法']:
       itchat.send('%s: %s' % (msg['Type'], msg['Text']), 'filehelper')



@itchat.msg_register('Text', isGroupChat=True)
def text_replys(msg):
    if str(msg['Text']) in [u'开始']:
      itchat.send(u'输入 碰运气 看看 ，满分100', msg['FromUserName'])
    elif str(msg['Text']) in [u'碰运气']:
      itchat.send(str(random.randrange(100)), msg['FromUserName'])
    elif str(msg['Text']) in [u'语法']:
      itchat.send(str(q[random.randrange(len(q))]), msg['FromUserName'])
    elif str(msg['Text']) in [u'美女']:
      itchat.send_image(u'/home/yangjc/图片/' + str(random.choice(os.listdir("/home/yangjc/图片/"))),msg['FromUserName'])


itchat.auto_login(enableCmdQR=2,hotReload=True)
itchat.run(debug=True)
'''

for i in range(len(q)):
    msgs = q[i]
    itchat.send(msgs, toUserName='filehelper')
    time.sleep(5)
'''