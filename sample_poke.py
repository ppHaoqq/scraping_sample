
import time
import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient

main_url = 'https://yakkun.com/swsh/zukan/'


def extract_key(url):
    m = re.search(r'([^/])+$', url)
    _key = m.group(0)
    return _key

#クライアント取得
client = MongoClient('localhost', 27017)
#データベース取得（pokemon）
db = client.pokemon
#テーブル取得(pokedb)
collection = db.pokedb
#collection.delete_many({})=>練習用に都度削除するための構文
collection.create_index('key', unique=True)

r = requests.get(main_url)
soup = bs(r.content, 'html.parser')
data = soup.select('#contents > div.pokemon_list_box > ul.pokemon_list > li > a')

#count = 0
for _url in data:
        url2 = urljoin(main_url, _url.get('href'))
        key = extract_key(url2)
        exist_poke = collection.find_one({'key': key})
        if not exist_poke:
            time.sleep(2)
            r2 = requests.get(url2)
            soup2 = bs(r2.content, 'html.parser')
            #soup5までいらんクラスの削除、勝手にsoup2も変更される
            soup3 = soup2.find_all(class_='needless')
            for soup4 in soup3:
                soup5 = soup4.decompose()
            poke = {
                'key': extract_key(url2),
                'name': soup2.select('.head > th[colspan="2"]')[0].text,
                'weight': soup2.select('.center > td > ul > li')[0].text,
                'h': int(soup2.select('#stats_anchor > table > tr:nth-child(2) > td.left')[0].text),
                'a': int(soup2.select('#stats_anchor > table > tr:nth-child(3) > td.left')[0].text),
                'b': int(soup2.select('#stats_anchor > table > tr:nth-child(4) > td.left')[0].text),
                'c': int(soup2.select('#stats_anchor > table > tr:nth-child(5) > td.left')[0].text),
                'd': int(soup2.select('#stats_anchor > table > tr:nth-child(6) > td.left')[0].text),
                's': int(soup2.select('#stats_anchor > table > tr:nth-child(7) > td.left')[0].text)
            }
            collection.insert_one(poke)
            #count += 1
        else:
            print(collection.find_one({'key': key}))