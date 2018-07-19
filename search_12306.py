# coding:utf-8
# 首先，要获取数据，就得知道12306的接口，而拿到接口就要使用抓包的方式：可使用浏览器自带的检查功能或fiddler
# 获取的接口为：Request URL: https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-08-03&
# leftTicketDTO.from_station=LMH&leftTicketDTO.to_station=HZH&purpose_codes=ADULT


# leftTicketDTO.train_date=2018-08-03：查询日期；
# leftTicketDTO.from_station=LMH：出发地
# leftTicketDTO.to_station=HZH&purpose_codes=ADULT：目的地
# purpose_codes=ADULT：车票类型


# 因为URL中地点都是字母，所以要拿到所有车站信息列表才能构造请求，查看源代码获取：
# https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9059


import re
import requests
import pprint
import json
import prettytable as pt
# from __future__ import unicode_literals
import sys
# 打开字典：
f = open('station_names.txt', 'r')
a = f.read()
station_name = eval(a)
f.close()

start = input("起始点：")
start_eng = station_name[start]

end = input("目的地：")
end_eng = station_name[end]

date = input("出发时间：")
d = str('2018-') + str(date)
print("正在查询...")

# 匹配网址：
url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date='+d+'&leftTicketDTO.from_station='+start_eng\
    +'&leftTicketDTO.to_station='+end_eng+'&purpose_codes=ADULT'
r = requests.get(url)
# print(r.status_code)
# pprint.pprint(r.text)


# 解析结果(返回的是一个列表)：
# results = r.json()
results = r.json()['data']['result']
# print(results)

# 创建表格：
table = pt.PrettyTable(encoding=sys.stdout.encoding)
# split() 方法通过指定分隔符对字符串进行分割并返回一个列表，默认分隔符为所有空字符，包括空格、换行(\n)、制表符(\t)等：
table.field_names = (["车次", "起始车站", "终点站", "出发地", "目的地", "开始时间", "到达时间", "经历时间", "一等座",
                      "二等座", "硬座", "无座"])

for result in results:
    data_list = result.split("|")
    station_train_code = data_list[3]
    # from_station = data_list[4]
    # to_station = data_list[5]

    # 由value值获取key值：
    from_station = list(station_name.keys())[list(station_name.values()).index(data_list[4])]
    to_station = list(station_name.keys())[list(station_name.values()).index(data_list[5])]
    start_station = list(station_name.keys())[list(station_name.values()).index(data_list[6])]
    end_station = list(station_name.keys())[list(station_name.values()).index(data_list[7])]

    start_time = data_list[8]
    arrive_time = data_list[9]
    total_time = data_list[10]
    one_seat = data_list[-6]
    second_seat = data_list[-7]
    yingzuo = data_list[-11]
    no_seat = data_list[-8]

    # print(from_station)

    table.add_row([station_train_code, from_station, to_station, start_station, end_station, start_time, arrive_time,
                   total_time, one_seat, second_seat, no_seat, yingzuo])
table.align = 'c'
table.set_style(pt.PLAIN_COLUMNS)
print(len(results))
print(table)



















