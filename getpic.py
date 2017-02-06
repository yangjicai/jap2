#/usr/bin/python3
#coding=utf8

import requests
import random
from bs4 import BeautifulSoup
from time import sleep


def getbeauty():
    url = 'https://moonhug.com/category/hot-sexy-asian-girls/page/' + str(random.randint(1, 80))
    response = requests.get(url)
    bs4 = BeautifulSoup(response.text,"html.parser")
    alist = bs4.find_all('a')
    linklist =  [ x['href']  for x in alist if x.find('span',attrs= {'class':'overlay-img'}) ]
    url = linklist[random.randint(0,len(linklist))]
    print(url)
    response = requests.get(url)
    bs4 = BeautifulSoup(response.text, "html.parser")
    alist = bs4.find_all('div',attrs={'class':'entry-content'})[0].find_all("a")

    linklist = [ link for link in [a['href'] for a in alist if a.find('img')] if link not in ['http://lp.moonhug.com']]
    print(linklist)
    url = linklist[random.randint(0, len(linklist)-1)]
    imgfile = requests.get(url)
    fp = open("/tmp/now.jpg", 'wb')
    fp.write(imgfile.content)
    fp.close()

