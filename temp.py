#/usr/bin/python3
#coding=utf8
import requests
from bs4 import BeautifulSoup

def getbeauty(i):
    imglist = []
    try:
        url = 'https://moonhug.com/category/asian-girls-wallpapers/page/' + str(i)
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
                print(tmpimglist)
                imglist.extend(tmpimglist)

        return imglist
    except:
        print("something is wrong")

getbeauty(1)

