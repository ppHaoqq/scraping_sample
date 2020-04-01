"""
pyquery を試そう
"""
from urllib.parse import urljoin
import requests
from pyquery import PyQuery as pq

url = 'https://gihyo.jp/dp'
r = requests.get(url).text

d = pq(r)
d.make_links_absolute(url)

for a in d('#listBook>li>a[itemprop="url"]'):
    url = d(a).attr('href')
    p = d(a).find('p[itemprop="name"]').eq(0)
    title = p.text()

    print(url, title)