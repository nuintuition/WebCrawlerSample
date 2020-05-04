import requests
import time
from bs4 import BeautifulSoup
import mssqldb
from random import randint

url="https://www.ptt.cc/bbs/Gossiping/index.html"
headers = {
    "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
}

def get_all_href(url):
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text,"html.parser")
    results = soup.select("div.r-ent")
    article_href = []
    for item in results:
        title_item = item.select_one("div.title a")
        if title_item is None:
            title_item = item.select_one("div.title")
        name_item = item.select_one("div.meta").select_one("div.author")
        # 取出本頁文章的標題、連結、作者
        item_href = { "title":title_item.text.strip(),
                    "url":'https://www.ptt.cc' + title_item.get("href") if not title_item.get("href") is None else "",
                    "name":name_item.text}
        article_href.append(item_href)
    return article_href

# 簡單設定最多爬幾頁
number = 2
for page in range(1,number):
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text,"html.parser")
    btn = soup.select('div.btn-group > a')
    up_page_href = btn[3]['href']
    next_page_url = 'https://www.ptt.cc' + up_page_href
    ret = get_all_href(url)
    sqlValue = list(map(lambda d: (url,d["title"],d["name"], d["url"]), ret))
    url = next_page_url
    # 儲存ptt上的文章標題、連結、作者
    sql = "insert into [PTable]([IndexUrl], [title], [name], [url]) VALUES(?, ?, ?, ?)"
    mssqldb.cursor.executemany(sql,sqlValue)
    mssqldb.cnxn.commit()
    # 隨機停留一個時間再繼續執行
    c = randint(10, 100)
    f = float(c)
    time.sleep(f)

