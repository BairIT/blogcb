
import datetime
from os.path import isfile
import random
import time
import requests as req
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
from config import token, proxyies, channel, pattern

TOKEN = token
pattern = pattern


def matcher(new, link):
    with open('news.txt', 'r+') as file:
        j = file.readlines()
        if (new + '\n') in j:
            pass
        else:
            file.write(new + '\n')
            file.write(link + '\n')
            file.write(str(datetime.datetime.now()))
            send_telegram(new, link)


def check(link):
    for i in pattern:
        if re.search(i, link):
            return link
        pass
    pass


def send_telegram(new, link):
    channel_id = channel
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(TOKEN)
    resp = req.post(url, data={
        "chat_id": channel_id,
        "text": ' ! ' + new + ' ! '+ '\n' +
                '! ' + link + ' ! ' + '\n'+
                ' ! ' + str(datetime.datetime.now()) + ' ! '
             })


def main():
    url = 'https://blog.coinbase.com/feed'
    ua = UserAgent()
    headers = {
        'user-agent': ua.random
    }
    proxy_source = proxyies
    proxies = {
        'https': random.choice(proxy_source)
    }
    try:
        response = req.get(url, headers=headers, proxies = proxies)
        print('!!!!'*10, response.status_code, '!!!'*10)
        print('proxy : ', proxies['https'])
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            new = soup.find('item')
            new_title = new.find('title').text
            link = new.find('link').text
            if check(link):
                matcher(new_title, link)
            pass
        else:
            pass
    except Exception as err:
        with open('Error.txt', 'w') as fil:
            fil.write(str(err))
            print(err)
            time.sleep(5)


if __name__=='__main__':
    if not isfile('news.txt'):
        open('news.txt', 'w')
    else:
        pass
    count = 0
    while True:
        count += 1
        tim = datetime.datetime.now()
        main()
        print('цикл : ', count)
        tim2 = datetime.datetime.now()
        delta = tim2 - tim
        print()
        print('time : ', delta.seconds)
        if delta.seconds > 120:
            pass
        continue
