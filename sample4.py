"""
bs を試そう
"""
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup as bs

url = 'https://gihyo.jp/dp'
r = requests.get(url).text
soup = bs(r, 'html.parser')

for a in soup.select('#listBook>li>a[itemprop="url"]'):
    url = urljoin(url, a.get('href'))
    p = a.select('p[itemprop="name"]')[0]
    title = p.text

    print(url, title)