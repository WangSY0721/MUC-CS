# -*- coding:utf8 -*-

import urllib.request
from bs4 import BeautifulSoup
import re

List_HouseAll  = []         #总表，所有房屋信息。二维列表。
TotalCountShow = 2          #需要显示的记录总数，如果为0，则全部显示。
CurCountShow = 0            #当前记录数

# 链接地址解析-------------------------<链家房价>------------------------------------------------
url = "https://bj.lianjia.com/ershoufang/rs%E6%B0%91%E6%97%8F%E5%A4%A7%E5%AD%A6/"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html.read().decode('utf-8'), "lxml")

# 找到【第1层标签：<div class="info clear">】-------------------------------------------------------------------------
tag1_all = soup.find_all( "div", {"class":"info clear"} )
                                    # 单个或多个属性都可用字典形式,{"class":"item" ,"data-houseid":"101111735457"}
                                    # find_all返回满足条件的【所有】结果，是一个列表。
                                    # find返回满足条件的【第1个】结果。
# print(tag1_all)

print("----------------------------------------------------------------------------------------------------")
# 遍历find_all找到的所有结果-------------------------------------------------------------------------
for tag1_InfoClear in tag1_all:
    #【第2层标签：<div class="title">】：获取房屋名称信息-------------------------------------------------------------------------
    tag2_title=tag1_InfoClear.find("div", class_="title")
    print("房屋名称：", tag2_title.text)            #如果是tag2_title.text，则结果不同

    #【第2层标签：<div class="flood">】：获取房屋位置信息-------------------------------------------------------------------------
    tag2_flood=tag1_InfoClear.find("div", class_="flood")             #找标签flood、positionInfo都可以
    # tag2_flood=tag1_InfoClear.find("div", class_="positionInfo")
        #虽然<div class="positionInfo">是第三层，但在<div class="info clear">这个第一层标签下，是唯一的。

    #【第4层标签】-------------------------------------------------------------------------
    #<a>是第4层，可以在"flood"下找，也可以在"positionInfo"下找。只要能确保唯一性。
    print("位置：", end="")

    #可替换代码段
    tag4_a=tag2_flood.find_all("a")
    str_pos=""                          #存入字符串，在后面要添加至列表
    for tag4_a1 in tag4_a:              #在【"positionInfo"】下有多个【<a>】，所以需要遍历所有【<a>】标签
        str_pos=str_pos+tag4_a1.text
    print(str_pos)

    # 如果<flood>标签下的所有文本都需要，可以直接提取，不必层层找。这面这段代码，可以替换上面的5行代码段。
    # 注意：和上面代码提取的文本是有区别的。
    # str_pos=""
    # str_pos=str_pos+tag2_flood.text
    # print(str_pos)

    tag2_houseInfo=tag1_InfoClear.find("div", class_="houseInfo")
    str_pos=str_pos+tag2_houseInfo.text     #【"houseInfo"】标签只有一个，不需要遍历，只接提取，用find。
    print(str_pos)            #这行的显示结果中有竖线【|】，在最终显示中不能有它。
    print("----------------------------------------------------------------------------------------------------")

    # 显示指定个数的记录
    if TotalCountShow > 0:
        CurCountShow = CurCountShow + 1
        if CurCountShow == TotalCountShow:
            break
