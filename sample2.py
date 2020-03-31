"""
技評にある本のURLとタイトルがjsonファイルで出力されるよ

"""
import requests
import lxml.html
import csv
import json

url = 'https://gihyo.jp/dp'

r = requests.get(url)
rhtml = r.text

html = lxml.html.fromstring(rhtml)
html.make_links_absolute(url)

with open('booklist.json', 'w', newline="")as f:

    for a in html.cssselect('#listBook>li>a[itemprop="url"]'):
        book_url = a.get('href')

        p = a.cssselect('p[itemprop = "name"]')[0]
        title = p.text_content()

        json.dump([{'url': book_url, 'title': title}], f, ensure_ascii=False, indent=2)


