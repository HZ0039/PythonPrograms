from urllib import request
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pymysql,re

list = []
city_list = []
price_list = []
result = []
province_list = []
city2_list = []
town_list = []

response = request.urlopen("https://www.qinbing.cn/")
htmltext = response.read().decode()
partten = "style=\"margin-right: 0px;width: 280px;\".*元/斤"
re_list = re.findall(partten, htmltext)
for item in re_list:
    item = item.split(">")[1]
    list.append(item)

partten = "\d.*斤"
for tmp in list:
    price_item = re.findall(partten, tmp)
    price_list.append(price_item[0])
    city_item = re.sub("\d.*斤", "", tmp)
    city_list.append(city_item)
# print(city_list,price_list)

for n in range(len(price_list)):
    cityitemlist = city_list[n].split(",")
    citylen = len(cityitemlist)
    province_list.append(cityitemlist[0])
    city2_list.append(cityitemlist[1])
    if citylen == 3:
        town_list.append(cityitemlist[2])
    else:
        town_list.append("")

dic = {
    "province": province_list,
    "city": city2_list,
    "town": town_list,
    "price": price_list
}
df = pd.DataFrame(dic)

mysqlconnect = create_engine('mysql+pymysql://root@localhost:3306/pythontask?charset=utf8')
pd.io.sql.to_sql(df, "HZ0039crawl", mysqlconnect, "pythontask")