"""
DB保存のためにmysql練習　参考URL　https://qiita.com/valzer0/items/2f27ba98397fa7ff0d74
"""
import mysql.connector as mydb

conn = mydb.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    password='w9478zqh',
    database='scraping'
)
conn.ping(reconnect=True)

c = conn.cursor()

c.execute('DROP TABLE IF EXISTS `cities`')
c.execute(
    """
    CREATE TABLE IF NOT EXISTS `cities`(
    `rank` int(11),
    `city` varchar(50) not null,
    `population` int(11) not null
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
    """)
c.execute("INSERT INTO cities VALUES(%s, %s, %s);", (1, '上海', 24150000))
c.execute("INSERT INTO cities VALUES(%(rank)s, %(city)s, %(population)s)", {'rank': 2, 'city': 'カラチ', 'population': 23500000})
c.executemany("INSERT INTO cities VALUES(%(rank)s, %(city)s, %(population)s)",[
              {'rank': 3, 'city': '北京', 'population': 215160000},
              {'rank': 4, 'city': '天津', 'population': 14722100},
              {'rank': 5, 'city': 'イスタンブル', 'population': 14160467}])

c.execute("SELECT * FROM cities")
for row in c.fetchall():
    print(row)

c.close()
conn.close()