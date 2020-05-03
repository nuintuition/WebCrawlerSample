import mssqldb
from bs4 import BeautifulSoup
import requests
import datetime

url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
headers = {
    "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
}

response = requests.get(url, headers = headers)

soup = BeautifulSoup(response.text,"html.parser")
table = soup.select("table")[1]

sql_value =[]
for tr in table.select("tr"):
    try:
        stock_id = tr.select("td")[0].text.split("\u3000")[0]
        stock_name = tr.select("td")[0].text.split("\u3000")[1]
        stock_date = tr.select("td")[2].text
        sql_value.append((stock_id,stock_name,stock_date))
    except:
        print(tr)

sql = "insert into ListedCompany (id,name,date) VALUES(?,?,?)"
mssqldb.cursor.executemany(sql,sql_value)
mssqldb.cursor.commit()