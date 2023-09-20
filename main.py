import requests
from bs4 import BeautifulSoup
import lxml
import json


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}
fests_urls = []
for i in range(0,360,24):
# for i in range(0,24,24):
    url = f'https://www.skiddle.com/festivals/search/?fest_name=&maxprice=500&o={i}'

    req = requests.get(url=url, headers=headers)
    src = req.text

    with open(f'data/index_{i}.html', 'w') as file:
        file.write(src)

    with open(f'data/index_{i}.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    cards = soup.find_all('a', class_='card-details-link')

    for item in cards:
        fest_url = 'https://www.skiddle.com' + item.get('href')
        fests_urls.append(fest_url)
count = 0
fest_list_result = []

for url in fests_urls:
    count += 1
    print(count)
    req = requests.get(url=url, headers=headers)
    try:
        soup = BeautifulSoup(req.text, 'lxml')
        fest_url = url
        fest_name = soup.find('h1',class_='MuiTypography-root MuiTypography-body1 css-r2lffm').text
        fest_date = soup.find('div',class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol').text

        fest_list_result.append(
            {
                "Fest_url":fest_url,
                "Fest_name":fest_name,
                "Fest_date":fest_date
            }
        )
    except(Exception) as ex:
        print(ex)
        print('Возникал ошибка')
with open ('data/fest_list_result.json', 'a', encoding='utf-8') as file:
    json.dump(fest_list_result, file, indent=4, ensure_ascii=False)
