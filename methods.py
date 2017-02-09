#/usr/bin/python3
#coding=utf8
import xml.etree.ElementTree as etree
import requests
import random
import pymysql
import re
from bs4 import BeautifulSoup



def getcityid(city):
    city_url = 'http://weather.livedoor.com/forecast/rss/primary_area.xml'
    response = requests.get(city_url)
    root = etree.fromstring(response.text)
    for cityname in root.iter('city'):
        citys = cityname.attrib
        if citys['title'] in city:
           return citys['id']
    for topname in root.iter('pref'):
        citys = topname.attrib
        if citys['title'] in city:
           topcity = topname.find('city')
           subcitys = topcity.attrib
           return subcitys['id']
 #          print(citys)
 #          return citys['id']
    return  '120010'


def getweather(city):
    id = getcityid(city)
    json_url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
    payload = {'city':id}
    response = requests.get(json_url,params=payload)
    json = response.json()
    text = json['description']['text']
    return text

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

def oldgetbeauty():
    url = 'https://moonhug.com/category/hot-sexy-asian-girls/page/' + str(random.randint(1, 80))
    response = requests.get(url)
    bs4 = BeautifulSoup(response.text,"html.parser")
    alist = bs4.find_all('a')
    linklist =  [ x['href']  for x in alist if x.find('span',attrs= {'class':'overlay-img'}) ]
    url = linklist[random.randint(0,len(linklist))]
    print(url)
    response = requests.get(url)
    bs4 = BeautifulSoup(response.text, "html.parser")
    alist = bs4.find('div',attrs={'class':'entry-content'}).find_all("img")

    linklist = [ link for link in [a['src'] for a in alist ] if link not in ['https://moonhug.com/wp-content/themes/annina/ad/cpaimg/63.jpg']]
    if len(linklist)-1 > 0:
        url = linklist[random.randint(0, len(linklist)-1)]
    else:
        url = 'https://pic.moonhug.com/uploads/2014/09/rosimm-985-001.jpg'

    imgfile = requests.get(url)
    fp = open("/tmp/now.jpg", 'wb')
    fp.write(imgfile.content)
    fp.close()

def getyufa():
    try:
        conn = pymysql.connect('192.168.11.2', 'weixin', 'weixin', 'weixin', charset='utf8')
    except:
        print("I am unable to connect to the database.")
    cur = conn.cursor()
    cur.execute("select * from yufalist")
    rows = cur.fetchall()
    yufa = rows[random.randrange(0,len(rows))][1]

    cur.close()
    if conn is not None:
        conn.close()
    return yufa


def getbeauty(filename):
    try:
        conn = pymysql.connect('192.168.11.2', 'weixin', 'weixin', 'weixin', charset='utf8')
    except:
        print("I am unable to connect to the database.")
    cur = conn.cursor()
    cur.execute("select src from imglist where id = {}".format(random.randint(1,80000)))
    rows = cur.fetchone()
    url = rows[0]
    imgfile = requests.get(url)
    fp = open(filename, 'wb')
    fp.write(imgfile.content)
    fp.close()
    cur.close()
    if conn is not None:
        conn.close()


def gettangshi():
    try:
        conn = pymysql.connect('192.168.11.2', 'weixin', 'weixin', 'weixin', charset='utf8')
    except:
        print("I am unable to connect to the database.")
    cur = conn.cursor()
    cur.execute("select title,author,content from tangshilist where id = {}".format(random.randrange(0,393)))
    rows = cur.fetchone()
    shici = '\n'.join(rows)

    cur.close()
    if conn is not None:
        conn.close()
    return shici