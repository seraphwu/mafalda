import requests
from bs4 import BeautifulSoup
url = "https://www.mirrormedia.mg/section/mafalda"

web = requests.get(url)
web.encoding = 'UTF-8'
soup = BeautifulSoup(web.text, "html.parser")
mafalda=soup.find_all('a',class_='kELWiM')
# .gLDNwx 標題
# .tPyZl 內文
#print(mafalda)
#print('\n----------\n')
url = 'https://notify-api.line.me/api/notify'
token = 'kv0vadXG0TWcvq0pIk0BhR6mOkePNhkacxrtlmyaVia'
headers = {
    'Authorization': 'Bearer ' + token    # 設定權杖
}
for i in mafalda:
    mafalda1=i.find('div',class_='gLDNwx').get_text()
    mafalda2=i.find('div',class_='tPyZl').get_text()
    text=mafalda1+'\n\n'+mafalda2
    #print('\n----------\n')
    data = {'message':text}     # 設定要發送的訊息
    data = requests.post(url, headers=headers, data=data)
'''
title=soup.select('main div .gLDNwx')
sp = soup.select('main div .tPyZl')
#sp = txt.select('main div .gLDNwx')
#txtt = sp.find('a',class_='kELWiM')
print(soup.select('main div .gLDNwx'))
print('\n----------\n')
print(soup.select('main div .tPyZl'))
print('\n----------\n')
'''


'''
data = {
    'message':'測試一下！'     # 設定要發送的訊息
}

data = requests.post(url, headers=headers, data=data)   # 使用 POST 方法
'''