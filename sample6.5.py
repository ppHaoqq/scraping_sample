"""
mongoDB使ってみよう
"""
import requests
import lxml.html
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.scraping
collection = db.books
collection.delete_many({})

url = 'https://gihyo.jp/dp'

r = requests.get(url)
rhtml = r.text
html = lxml.html.fromstring(rhtml)
html.make_links_absolute(url)

for a in html.cssselect('#listBook>li>a[itemprop="url"]'):
    book_url = a.get('href')

    p = a.cssselect('p[itemprop = "name"]')[0]
    title = p.text_content()

    collection.insert_one({'url': book_url, 'title': title})


cursor = collection.find()
for link in cursor.sort('_id'):
    print(link['_id'], link['url'], link['title'])