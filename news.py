import mssqldb
import requests
from bs4 import BeautifulSoup

site_url = 'https://news.cnyes.com'

url = site_url + '/news/cat/wd_stock'
headers = {
    "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
}

response = requests.get(url, headers = headers)

soup = BeautifulSoup(response.text,"html.parser")

div_tags = soup.select('div.theme-list div')

newsList = []
for news in div_tags:
    
    if not news.a:
        continue

    title = news.a.get('title')
    link = site_url + news.a.get('href')
    sub_category = news.select_one('div.theme-sub-cat').text

    newsList.append((title,link,sub_category))

sql = "insert into NEWS (title,link,subcategory) VALUES(?,?,?)"
mssqldb.cursor.executemany(sql,newsList)
mssqldb.cnxn.commit()


