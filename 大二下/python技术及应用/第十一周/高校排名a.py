import requests
from bs4 import BeautifulSoup

url = "http://www.gaosan.com/gaokao/43980.html"
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text

soup = BeautifulSoup(html, 'html.parser')

table = soup.find("table", {"width": "580px", "align": "center"})
rows = table.find_all("tr")

data = []
for row in rows[1:]:
    cols = row.find_all("td")
    cols = [col.text.strip() for col in cols]
    data.append(cols)

sorted_data = sorted(data, key=lambda x: float(x[7]))

for item in sorted_data:
    print(item)
