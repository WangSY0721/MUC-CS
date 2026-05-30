# -*- coding:utf8 -*-

import requests
from bs4 import BeautifulSoup
import re

List_HouseAll  = []         #总表，所有房屋信息。二维列表。
TotalCountShow = 2          #需要显示的记录总数，如果为0，则全部显示。
CurCountShow = 0            #当前记录数

# 链接地址解析-------------------------<链家房价>------------------------------------------------
url = "https://bj.lianjia.com/ershoufang/rs%E6%B0%91%E6%97%8F%E5%A4%A7%E5%AD%A6/"


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
r = requests.get(url, headers=headers)  ##通过get（）方法，加上要抓取的网页地址，就可以获得一个response对象，为了解决反爬机制，我们加上了header

from bs4 import BeautifulSoup  # 导入BeautifulSoup库
soup = BeautifulSoup(r.text, 'lxml')  # 把之前get到的对象作为一个参数传入BeautifulSoup（）函数，结果是生成了一个BeautifulSoup对象soup

# 找到【第1层标签：<div class="info clear">】-------------------------------------------------------------------------
tag1_all = soup.find_all( "div", {"class":"info clear"} )
                                    # 单个或多个属性都可用字典形式,{"class":"item" ,"data-houseid":"101111735457"}
                                    # find_all返回满足条件的【所有】结果，是一个列表。
                                    # find返回满足条件的【第1个】结果。
# print(tag1_all)

print("----------------------------------------------------------------------------------------------------")
# 遍历find_all找到的所有结果-------------------------------------------------------------------------
for tag1_InfoClear in tag1_all:
    print("房屋名称：", tag1_InfoClear)            #如果是tag2_title.text，则结果不同
