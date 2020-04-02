import mysql.connector as mydb
import time
import requests
import lxml.html

#一覧ページにアクセスしつつそのオブジェクトを他の関数に回すメイン関数
def main():
    session = requests.Session()
    r = requests.get('https://gihyo.jp/dp')
    urls = scrape_list_page(r)
    for url in urls:
        time.sleep(1)
        r = session.get(url)
        ebook = scrape_detail_page(r)
        print(ebook)
        #break


#詳細PのURLをスクレイプする関数
def scrape_list_page(response):
    html = lxml.html.fromstring(response.text)
    html.make_links_absolute(response.url)
    for a in html.cssselect('#listBook>li>a[itemprop="url"]'):
        url = a.get('href')
        yield url


#詳細Pをスクレイプする関数
def scrape_detail_page(response):
    html = lxml.html.fromstring(response.text)
    ebook = {
        'url': response.url,
        'title': html.cssselect('#bookTitle')[0].text_content(),
        'price': html.cssselect('.buy')[0].text.strip(),
        'content': [normalize_spaces(h3.text_content())for h3 in html.cssselect('#content>h3')],
    }
    return ebook


def normalize_spaces(s):
    return re.sub(r'\s+', '', s).strip()




if __name__ == '__main__':
    main()
