#/usr/bin/python3
#coding=utf8

import pymysql
import requests
import random
from bs4 import BeautifulSoup
from time import sleep
import queue
import threading
import time

def insertdb(list):
    try:
        conn = pymysql.connect('192.168.11.2', 'weixin', 'weixin', 'weixin', charset='utf8')
    except:
        print("I am unable to connect to the database.")

    cur = conn.cursor()



    query =  'INSERT INTO imglist (src) VALUES ( "{}");'

    i = 1
    try:
        for msg in list:
            data = (msg)
            str = query.format(msg)
            cur.execute(str.encode('utf-8'))
    except:
        print("can not insert")

    cur.close()
    conn.commit()
    if conn is not None:
        conn.close()


def getbeauty(i):
    imglist = []
    try:
        #url = 'https://moonhug.com/category/asian-girls-wallpapers/page/' + str(i)
        url = 'https://moonhug.com/category/hot-sexy-asian-girls/page/' + str(i)

        response = requests.get(url)
        bs4 = BeautifulSoup(response.text,"html.parser")
        alist = bs4.find_all('a')
        linklist =  [ x['href']  for x in alist if x.find('span',attrs= {'class':'overlay-img'}) ]
        for link in linklist:
            response = requests.get(link)
            bs4 = BeautifulSoup(response.text, "html.parser")
            pagelist = bs4.find('div',attrs={'class':'page-links'}).find_all('a')
            pagelist =[page['href'] for page in pagelist]
            for page in pagelist:
                response = requests.get(page)
                bs4 = BeautifulSoup(response.text, "html.parser")
                alist = bs4.find_all('div',attrs={'class':'entry-content'})[0].find_all("a")
                tmpimglist = [ link for link in [a['href'] for a in alist if a.find('img')] if link not in ['http://lp.moonhug.com']]

                imglist.extend(tmpimglist)
        print("get {} imgs".format(len(imglist)))
        return imglist
    except:
        print("something is wrong")



exitFlag = 0

class myThread(threading.Thread):
   def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
   def run(self):
      print ("Starting " + self.name)
      process_data(self.name, self.q)
      print ("Exiting " + self.name)

def process_data(threadName, q):
   while not exitFlag:
      if not workQueue.empty():
         data = q.get()
         print ("%s processing %s" % (threadName, data))
         list = getbeauty(data)
         print ("%s processing %s done" % (threadName, data))
         insertdb(list)
      else:
         time.sleep(1)


threadList = range(1,20)
nameList = range(1,80)
workQueue = queue.Queue()
threads = []
threadID = 1

# Create new threads
for tName in threadList:
   thread = myThread(threadID, tName, workQueue)
   thread.start()
   threads.append(thread)
   threadID += 1

# Fill the queue
for word in nameList:
   workQueue.put(word)

# Wait for queue to empty
while not workQueue.empty():
   pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
   t.join()
print ("Exiting Main Thread")





