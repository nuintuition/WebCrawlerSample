import mssqldb
import requests
import json

url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20200509&stockNo=2330&_=1589030292435"
headers = {
    "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
}

response = requests.get(url, headers = headers)
data = json.loads(response.text)["data"]

sql = "insert into ExchangeReport (companyId,日期,成交股數,成交金額,開盤價,最高價,最低價,收盤價,漲跌價差,成交筆數)\
     VALUES(2330,?,?,?,?,?,?,?,?,?)"
sqlValue = list(map(lambda d: tuple(d), data))

mssqldb.cursor.executemany(sql,sqlValue)
mssqldb.cnxn.commit()
