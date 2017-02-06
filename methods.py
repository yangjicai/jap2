#/usr/bin/python3
#coding=utf8
import xml.etree.ElementTree as etree
import requests
import random
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



def getimg():
    imgs = requests.get("http://meinv.tuku.com/index_" + str(random.randint(2,49)) + ".html" )
    soup = BeautifulSoup(imgs.text,"html.parser")
    divs = soup.find_all("div",attrs={'class':'pic'})
    sub = divs[random.randrange(len(divs))].find('a')
    url = sub['href']
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    bigpic = soup.find("img",attrs={'id':'bigPic'})
    r = requests.get(bigpic['src'])
    fp = open("/tmp/now.jpg", 'wb')
    fp.write(r.content)
    fp.close()
