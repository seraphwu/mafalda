import requests
from bs4 import BeautifulSoup
import datetime
from datetime import datetime
url = "https://www.mirrormedia.mg/section/mafalda"
web = requests.get(url)
web.encoding = 'UTF-8'
soup = BeautifulSoup(web.text, "html.parser")
mafalda=soup.find_all('a',class_='kELWiM')
# .gLDNwx 標題
# .tPyZl 內文

now = datetime.now()
time_string = now.strftime("%Y-%m-%d") # from https://blog.csdn.net/weixin_35750747/article/details/129568968
filename = "mafalda-" + time_string + ".txt"
path = filename
f = open(path, 'a') # from https://shengyu7697.github.io/python-write-text-file/
for i in mafalda:
    mafalda1=i.find('div',class_='gLDNwx').get_text()
    mafalda2=i.find('div',class_='tPyZl').get_text()
    text=mafalda1+'\n\n'+mafalda2
    f.write(text)
    f.write('\n----------\n')