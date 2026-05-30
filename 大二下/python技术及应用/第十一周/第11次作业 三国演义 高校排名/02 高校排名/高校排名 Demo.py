# -*- coding:utf8 -*-

import urllib.request
from bs4 import BeautifulSoup

# 链接地址解析-------------------------------------------------------------------------
url = "http://www.gaosan.com/gaokao/43980.html"

HttpResponseObject = urllib.request.urlopen(url)
# print(HttpResponseObject)
strHtml=HttpResponseObject.read()
soup = BeautifulSoup(strHtml.decode('utf-8'), "lxml")

# find_all、find的区别
# find_all： 返回满足条件的【所有】结果
# find：     返回满足条件的【第1个】结果

# 找到第一层父标签------------------------<tbody>------------------------------------------------
# 如果结果唯一，可以用它。
# data = soup.find_all("tbody")           #tbody:table body
# print("tbody长度：",len(data))
# print(">>>>",data)


# 找到第二层父标签------------------------<table width="580px" align="center">------------------------------------------------
data = soup.find_all("table", {"width":"580px", "align":"center"} )
# print("table长度：",len(data))
# print(">>>>:",data)

# quit()

#从<table>标签开始找
for data1 in data:  #逐一处理列表中的所有元素
    # print(data1)
    # continue
    for tbody in data1:         # tbody标签
        # print("【tbody:】",tbody)
        for tr in tbody:        # tr标签
            print("【tr:】", tr)
            for td in tr:       # td标签
                print(td.text,end="")
            print("\n---------------------------------------------------")

