import requests
from bs4 import BeautifulSoup
import re

List_HouseAll = []        
TotalCountShow = 2
CurCountShow = 0

url = "https://bj.lianjia.com/zufang/rs%E6%B0%91%E6%97%8F%E5%A4%A7%E5%AD%A6/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
r = requests.get(url, headers=headers)

from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, 'lxml')

tag1_all = soup.find_all( "div", {"class":"content__list--item"} )

print("----------------------------------------------------------------------------------------------------")
for house in tag1_all:
    list1 = []
    title = house.find('a', class_='twoline').get_text().strip()
    location = house.find('p', class_='content__list--item--des').get_text()
    price_total = house.find('span', class_='content__list--item-price').get_text().strip()

    price_total_num = int(re.findall(r'\d+', price_total)[0])
    location = location
    local = ""
    location = location.split('/')
    for i in location:
        i = i.replace('\n',' ')
        local = local + re.sub(' *','',i)+" "
    area1 = (re.findall(r'\d+\.?\d*㎡', local)[0])
    area = float(re.findall(r'\d+\.?\d*', area1)[0])
    list1.append({
        "名称": title,
        "位置":local,
        "面积":area,
        "总价":price_total_num
    })
    print(f"名称: {title}")
    print(f"位置: {local}")
    print(f"面积: {area1}")
    print(f"总价: {price_total}")
    print("-" * 40)
    List_HouseAll.append(list1)