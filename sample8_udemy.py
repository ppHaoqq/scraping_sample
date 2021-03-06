import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime


def get_udemy_info():
    url = 'https://scraping-for-beginner.herokuapp.com/udemy'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    #名前を取得
    name = soup.select('body > div.row > div > div:nth-child(2) > div > div > div.card-image > span')[0].text
    #登録者を取得
    num = soup.select('body>div.row>div>div:nth-child(2)>div>div>div.card-action>p.subscribers')[0].text
    n_subscribers = int(num.split('：')[1])
    #レビューを取得
    n_reviews = int(soup.select('.reviews')[0].text.split('：')[1])
    results = {'name': name, 'n_subscribers': n_subscribers, 'n_reviews': n_reviews}
    return results

#dfにファイルを読み込む
def save_csv():
    df = pd.read_csv('assets/udemy_data.csv')
    d = datetime.datetime.today().strftime('%Y/%m/%d')

    _results = get_udemy_info()
    n = _results['name']
    s = _results['n_subscribers']
    r = _results['n_reviews']

    #csvoの中身と同じ形に成型
    new_data = pd.DataFrame([[d, s, r]], columns=['date', 'subsucribers', 'reviews'])

    #級データと新データを結合(=.concat)
    df = pd.concat([df, new_data])
    #csvに上書き
    df.to_csv('assets/udemy_data.csv', index=False)


if __name__ =='__main__':
    save_csv()