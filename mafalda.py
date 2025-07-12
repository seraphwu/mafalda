import requests, json, datetime # json added 20250521
from bs4 import BeautifulSoup
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
    mafalda1=i.find('div',class_='gLDNwx').get_text()  #瑪法達標題
    mafalda2=i.find('div',class_='tPyZl').get_text() #瑪法達內文
    mafaldacontent=mafalda1+'\n\n'+mafalda2
    # added 20250521 https://steam.oxxostudio.tw/category/python/example/line-requests.html 開始
    headers = {'Authorization':'Bearer Xig1kV3NBaGuzbhuM7aOQZ62dPR6d/L4belt/ELspv+/14ymMN5FJ7ad6APRSYhkKTMJs30Nb1m1plTHcyCzLLaGzXHDnUDb1nkvXE/IjqpZSRMbbFGr0keZwXPlVRu+ZUu0q1/gZ2XPC8f1bQmJCAdB04t89/1O/w1cDnyilFU=','Content-Type':'application/json'}
    body = {
    'to':'U16ef4f263d22028c4cc741b6a4b08d40',
    'messages':[{
            'type': 'text',
            'text': mafaldacontent
        }]
    }
    req = requests.request('POST', 'https://api.line.me/v2/bot/message/push',headers=headers,data=json.dumps(body).encode('utf-8'))
    # added 20250521 https://steam.oxxostudio.tw/category/python/example/line-requests.html 結束
    # 印出得到的結果
    print(req.text)
    f.write(mafalda1)
    f.write('\n')
    f.write(mafalda2)
    f.write('\n----------\n')