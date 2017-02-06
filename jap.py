#/usr/bin/python3
#coding=utf8
import requests
import itchat
import methods
import random


q = methods.getMsgList()
WIFE = 'fengyan959734'
CHATROOMNAME = "AAAAA"

#msg form mywife
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
        if '语法' in msg['Text']:
           tempstr = msg['Text']
           num = [int(s) for s in tempstr.split() if s.isdigit()]
           if len(num) > 0:
               itchat.send(str(q[num[0] + 1]), WIFE)
           else:
               itchat.send(str(q[random.randrange(len(q))]), WIFE)
        elif '天気' in msg['Text']:
            cityname = msg['Text']
            axx = methods.getweather(cityname)
            itchat.send(cityname + '\n' + axx, WIFE)
        elif '美女' in msg['Text']:
            methods.getbeauty()
            itchat.send_image('/tmp/now.jpg', 'filehelper')

#msgform
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_replys(msg):
    taget_chatroom = itchat.search_chatrooms(CHATROOMNAME)
    if taget_chatroom is None:
        print(u'没有找到群聊：' + CHATROOMNAME)

    chatroom_name = taget_chatroom[0]['UserName']

    if chatroom_name in msg['FromUserName'] or chatroom_name in msg['ToUserName']:
        if '开始' in msg['Text']:
          itchat.send(u'输入 碰运气 看看 ，满分100', chatroom_name)
        elif '碰运气' in msg['Text']:
          itchat.send(str(random.randrange(100)), chatroom_name)
        elif '语法' in msg['Text']:
          itchat.send(str(q[random.randrange(len(q))]), chatroom_name)
        elif '美女' in msg['Text']:
          methods.getbeauty()
          itchat.send_image('/tmp/now.jpg', chatroom_name)

        '''
          itchat.send_image(u'/home/pi/2jipic/' + str(random.choice(os.listdir("/home/pi/2jipic/"))),chatroom_name)
        elif '工口' in msg['Text']:
          itchat.send_image(u'/home/pi/3jipic/' + str(random.choice(os.listdir("/home/pi/3jipic/"))),chatroom_name)
'''


itchat.auto_login(enableCmdQR=2,hotReload=True)
itchat.run(debug=True)


