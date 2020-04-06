import time
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.pokemon
collection = db.pokedb
collection.delete_many({})

main_url = 'https://yakkun.com/swsh/zukan/'

r = requests.get(main_url)
soup = bs(r.content, 'html.parser')

data = soup.select('#contents > div.pokemon_list_box > ul.pokemon_list > li > a')

urls = []
count = 0
for _url in data:
    if count == 10:
        break
    else:
        time.sleep(1)
        urls.append(urljoin(main_url, _url.get('href')))
        count += 1

for url in urls:
    r2 = requests.get(url)
    soup2 = bs(r2.content, 'html.parser')

    name = soup2.select('.head > th[colspan="2"]')[0].text
    weight = soup2.select('#base_anchor > table > tr:nth-child(7) > td:nth-child(2) > ul > li:nth-child(1)')[0].text
    h = int(soup2.select('#stats_anchor > table > tr:nth-child(2) > td.left')[0].text)
    a = int(soup2.select('#stats_anchor > table > tr:nth-child(3) > td.left')[0].text)
    b = int(soup2.select('#stats_anchor > table > tr:nth-child(4) > td.left')[0].text)
    c = int(soup2.select('#stats_anchor > table > tr:nth-child(5) > td.left')[0].text)
    d = int(soup2.select('#stats_anchor > table > tr:nth-child(6) > td.left')[0].text)
    s = int(soup2.select('#stats_anchor > table > tr:nth-child(7) > td.left')[0].text)
    poke = {'name': name, 'weight': weight, 'h': h, 'a': a, 'b': b, 'c': c, 'd': d, 's': s}
    collection.insert_one(poke)

cursor = collection.find()
for link in cursor:
    print(link['name'])
