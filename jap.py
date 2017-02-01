#/usr/bin/python3
#coding=utf8

import os
import requests
import itchat
import time
import random
import re
from bs4 import BeautifulSoup
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

deepThought = ChatBot("deepThought", trainer='chatterbot.trainers.ChatterBotCorpusTrainer')
#deepThought.set_trainer(ChatterBotCorpusTrainer)
# 使用中文语料库训练它
deepThought.train("chatterbot.corpus.chinese")  # 语料库


def getMsgList():
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


q = getMsgList()
WIFE = 'XXXX'
CHATROOMNAME = "XXXX"

#msg form mywife
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    if WIFE in msg['FromUserName']:
        if u'语法' in msg['Text']:
           tempstr = msg['Text']
           num = [int(s) for s in tempstr.split() if s.isdigit()]
           if len(num) > 0:
               itchat.send(str(q[num[0] + 1]), WIFE)
           else:
               itchat.send(str(q[random.randrange(len(q))]), WIFE)

#msgform
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_replys(msg):
    taget_chatroom = itchat.search_chatrooms(CHATROOMNAME)
    if taget_chatroom is None:
        print(u'没有找到群聊：' + CHATROOMNAME)

    chatroom_name = taget_chatroom[0]['UserName']

    print(chatroom_name)
    print(msg['FromUserName'])
    if chatroom_name in msg['FromUserName']:
        if [u'开始'] in msg['Text']:
          itchat.send(u'输入 碰运气 看看 ，满分100', msg['FromUserName'])
        elif u'碰运气' in msg['Text']:
          itchat.send(str(random.randrange(100)), msg['FromUserName'])
        elif u'语法' in msg['Text']:
          itchat.send(str(q[random.randrange(len(q))]), msg['FromUserName'])
        elif u'美女' in msg['Text']:
          itchat.send_image(u'/home/yangjc/图片/' + str(random.choice(os.listdir("/home/yangjc/图片/"))),msg['FromUserName'])


itchat.auto_login(enableCmdQR=2,hotReload=True)
itchat.run(debug=True)

