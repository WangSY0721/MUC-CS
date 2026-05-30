from pypinyin import Style,pinyin
import re
import urllib.request
from bs4 import BeautifulSoup

url = "http://www.gaosan.com/gaokao/43980.html"

HttpResponseObject = urllib.request.urlopen(url)
strHtml=HttpResponseObject.read()
soup = BeautifulSoup(strHtml.decode('utf-8'), "lxml")

data = soup.find_all("table", {"width":"580px", "align":"center"} )

def printflist(list1):
    for i in range(len(list1)):
        print(list1[i])
for data1 in data:  #逐一处理列表中的所有元素
    for tbody in data1:
        list2 =[]
        i = 0
        for tr in tbody:
            if (i == 0):
                i += 1
                continue
            list1 = []
            for td in tr:
                list1.append(re.sub('<.*>|\s',"",td.text))
            list2.append(list1)
    list2.sort(key=lambda x:[pinyin(i, style=Style.TONE3) for i in x[1]])
    printflist(list2)
