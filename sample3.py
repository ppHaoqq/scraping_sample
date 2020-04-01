"""
クロール・スクレイプ・保存をメイン関数にひとまとめ
"""

import requests
import lxml.html
import csv

def main():
    url = 'https://gihyo.jp/dp'
    html = fetch(url)
    books = scrape(html, url)
    save('books.csv', books)


def fetch(url):
    r = requests.get(url)
    return r.text


def scrape(html, base_url):
    books = []
    html2 = lxml.html.fromstring(html)
    html2.make_links_absolute(base_url)

    for a in html2.cssselect('#listBook>li>a[itemprop="url"]'):
        book_url = a.get('href')

        p = a.cssselect('p[itemprop = "name"]')[0]
        title = p.text_content()

        books.append({'url': book_url, 'title': title})
    return books


def save(file_path, books):
    with open(file_path, 'w', newline="")as f:
        writer = csv.DictWriter(f, ['url', 'title'])
        writer.writeheader()
        writer.writerows(books)


if __name__ == '__main__':
    main()
