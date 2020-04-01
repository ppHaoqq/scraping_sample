"""
技評にある本のURLとタイトルがｃsvファイルで出力されるよ
"""
import requests
import lxml.html
import csv

url = 'https://gihyo.jp/dp'

r = requests.get(url)
rhtml = r.text

html = lxml.html.fromstring(rhtml)
html.make_links_absolute(url)

with open('booklist.csv', 'w', newline="")as f:
    writer = csv.writer(f)

    for a in html.cssselect('#listBook>li>a[itemprop="url"]'):
        book_url = a.get('href')

        p = a.cssselect('p[itemprop = "name"]')[0]
        title = p.text_content()

        writer.writerow([{'url': book_url, 'title': title}])


