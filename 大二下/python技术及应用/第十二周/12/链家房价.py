import requests
from bs4 import BeautifulSoup
import re

url = 'https://bj.lianjia.com/ershoufang/rs%E6%B0%91%E6%97%8F%E5%A4%A7%E5%AD%A6/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

houses = soup.find_all('div', class_='info clear')

house_list = []

for house in houses:
    title = house.find('div', class_='title').get_text().strip()
    location = house.find('div', class_='flood').get_text().strip()
    house_info = house.find('div', class_='address').get_text().strip()
    price_total = house.find('div', class_='totalPrice').span.get_text().strip()
    price_unit = house.find('div', class_='unitPrice').span.get_text().strip()

    price_total_num = int(re.findall(r'\d+', price_total)[0])
    price_unit_num = int(re.findall(r'\d+', price_unit)[0])
    area = float(re.findall(r'\d+\.?\d*', house_info)[0])
    house_type = house_info.split('|')[1].strip()

    house_list.append({
        '名称': title,
        '位置': location,
        '屋型': house_type,
        '面积': area,
        '单价': price_unit_num,
        '总价': price_total_num
    })

house_list = sorted(house_list, key=lambda x: x['总价'], reverse=True)

for house in house_list:
    print(f"名称: {house['名称']}")
    print(f"位置: {house['位置']}")
    print(f"屋型: {house['屋型']}")
    print(f"面积: {house['面积']} 平米")
    print(f"单价: {house['单价']} 元/平米")
    print(f"总价: {house['总价']} 万元")
    print("-" * 40)
