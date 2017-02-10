#/usr/bin/python3
#coding=utf8
import itchat
import methods
import random
import threading
import queue

inputimg = queue.Queue()
outputimg = queue.Queue()

filenames = ['/tmp/1.jpg','/tmp/2.jpg','/tmp/3.jpg','/tmp/4.jpg']
threads = []

def worker():
    while True:
        fileanme = inputimg.get()
        methods.getbeauty(fileanme)
        outputimg.put(fileanme)

for i in range(3):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for i in range(4):
    inputimg.put(filenames[i])

me = ''

#msg form mywife
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    if msg['ToUserName'] == 'filehelper':
        me = msg['FromUserName']
    if me in msg['FromUserName']:
        target = msg['ToUserName']
    else:
        target = 'filehelper'
    if  msg['Text'] == '/帮助':
        itchat.send(u'''
        我有如下功能：
        输入 /美女 我将发送一张美女图片
        输入 /语法 我将发送一条日语语法
        输入 /诗词 我将发送一首诗/词
        ''', target)
    if msg['Text'] == '/语法':
        itchat.send(methods.getyufa(), target)
    elif  msg['Text'] == '/美女':
        filename = outputimg.get()
        try:
            itchat.send_image(filename,target)
        except:
            pass
        inputimg.put(filename)
    elif  msg['Text'] == '/诗词':
        itchat.send_msg(methods.gettangshi(),target)

#msgform
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_replys(msg):
    if me in msg['FromUserName']:
        target = msg['ToUserName']
    else:
        target = msg['FromUserName']
    if msg['Text'] == '/帮助':
        itchat.send(u'''
        我有如下功能：
        输入 /碰运气 看看运气如何（满分100）
        输入 /美女 我将发送一张美女图片
        输入 /语法 我将发送一条日语语法
        输入 /诗词 我将发送一首诗/词
        ''', target)
    elif msg['Text'] == '/碰运气':
        itchat.send(str(random.randrange(100)), target)
    elif  msg['Text'] == '/语法':
        itchat.send(methods.getyufa(), target)
    elif msg['Text'] == '/美女':
        filename = outputimg.get()
        try:
            itchat.send_image(filename, target)
        except:
            pass
        inputimg.put(filename)
    elif  msg['Text'] == '/诗词':
        itchat.send_msg(methods.gettangshi(), target)

itchat.auto_login(enableCmdQR=2,hotReload=True)
itchat.send_msg('help','filehelper')

itchat.run(debug=False)

