import re
import time
import requests
import lxml.html
from pymongo import MongoClient


#一覧ページにアクセスしつつそのオブジェクトを他の関数に回すメイン関数
def main():
    client = MongoClient('localhost', 27017)
    collection = client.scraping.poke_db
    collection.create_index('key', unique=True)

    session = requests.Session()
    r = requests.get('https://yakkun.com/swsh/zukan/')
    urls = scrape_list_page(r)
    for url in urls:
        key = extract_key(url)
        poke = collection.find_one({'key': key})
        if not poke:
            time.sleep(2)
            r = session.get(url)
            poke = scrape_detail_page(r)
            collection.insert_one(poke)
        print(poke)
            #break



#詳細PのURLをスクレイプする関数
def scrape_list_page(response):
    html = lxml.html.fromstring(response.text)
    html.make_links_absolute(response.url)
    for a in html.cssselect('#contents > div.pokemon_list_box > ul.pokemon_list'):
        url = a.get('href')
        yield url


#詳細Pをスクレイプする関数
def scrape_detail_page(response):
    html = lxml.html.fromstring(response.text)
    poke = {
        'url': response.url,
        'key': extract_key(response.url),
        'name': html.cssselect('#base_anchor > table > tbody > tr.head > th')[0].text_content(),
        'h': html.cssselect('#stats_anchor > table > tbody > tr:nth-child(2) > td.left')[0].text_content(),
        'a': html.cssselect('#stats_anchor > table > tbody > tr:nth-child(3) > td.left')[0].text_content(),
        'b': html.cssselect('#stats_anchor > table > tbody > tr:nth-child(4) > td.left')[0].text_content(),
        'c': html.cssselect('#stats_anchor > table > tbody > tr:nth-child(5) > td.left')[0].text_content(),
        'd': html.cssselect('#stats_anchor > table > tbody > tr:nth-child(6) > td.left')[0].text_content(),
        's': html.cssselect('#stats_anchor > table > tbody > tr:nth-child(7) > td.left')[0].text_content(),
    }
    return poke


#urlから本の識別番号を抜いてkeyを作る関数
def extract_key(url):
    m = re.search(r'/([^/]+)$', url)
    return m.group(1)



if __name__ == '__main__':
    main()
