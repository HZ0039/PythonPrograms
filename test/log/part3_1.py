import re,os,sys,time
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pymysql

info_ip_list = []
info_time_list = []
info_request_list = []
info_referer_list = []
info_code_list = []
info_agent_list = []

logfile = open("access.log.txt", "r")
logdata = logfile.readlines()
logfile.close


# 获取ip
def getIp(line):
    info_ip_item = line.split(" - -")[0]
    info_ip_list.append(info_ip_item)


# 获取time
def getTime(line):
    __partten = ".*?\[(.*?)\].*?"
    info_time_item = re.findall(__partten, line)
    info_time_item = str(info_time_item).split(" ")[0]
    info_time_item = info_time_item.replace("['", "")
    b = time.strptime(info_time_item, "%d/%b/%Y:%H:%M:%S")
    info_time_item = str(b.tm_year) + "/" + str(b.tm_mon) + "/" + str(b.tm_mday) + " " + str(b.tm_hour) + ":" + str(
        b.tm_min) + ":" + str(b.tm_sec)
    info_time_list.append(info_time_item)


# 获取请求信息
def getRequest(line):
    info_request_item = line.split("\"")[1]
    info_request_list.append(info_request_item)


# 获取
def getReferer(line):
    info_referer_item = line.split("\"")[3]
    if len(info_referer_list) > 4:
        info_referer_list.append(info_referer_item)
    else:
        info_referer_list.append("")


# 获取状态码
def getCode(line):
    info_code_item = line.split("\"")[2]
    info_code_item = int(info_code_item.split(" ")[1])
    info_code_list.append(info_code_item)


# 获取用户代理
def getUseragent(line):
    info_agent_item = line.split("\"")[-2]
    info_agent_list.append(info_agent_item)


for line in logdata:
    getIp(line)
    getTime(line)
    getRequest(line)
    getReferer(line)
    getCode(line)
    getUseragent(line)

info_dic = {
    "ip": info_ip_list,
    "time": info_time_list,
    "request": info_request_list,
    "referer": info_referer_list,
    "code": info_code_list,
    "agent": info_agent_list
}

df = pd.DataFrame(info_dic)
mysqlconnect = create_engine('mysql+pymysql://root@localhost:3306/pythontask?charset=utf8')
pd.io.sql.to_sql(df, "HZ0039log", mysqlconnect, "pythontask")

# df.to_csv('df.csv', sep=',', header=True, index=False)
# print(df)