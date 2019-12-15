from bs4 import BeautifulSoup
import requests


log_url = 'https://pikabu.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
payload = {'username': 'Tunturuntun', 'password': 'P1k4buHu3bu'}
tags = {}
tag_count = 0

with requests.Session() as s:
    s.post(log_url, data=payload, headers=headers)

    for page_num in range(1, 6):
        #The account uses paged view with 20 posts per page
        resp = s.get(f'https://pikabu.ru/new?page={page_num}', headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        rows = soup.find_all('a', {"class" : "tags__tag", "data-tag" : True})
        for row in rows:
            tag = row.get_text()
            tag_count += 1
            if tag not in tags:
                tags[tag] = 1
            else:
                tags[tag] += 1

sorted_tags = sorted(tags.items(), key=lambda v: v[1])[-10:]
print("Top 10 tags:")
for i in sorted_tags[::-1]:
    print(i[0], i[1])
print("Total tags:", tag_count)

"""
Top 10 tags:
Длиннопост 19
Видео 13
Текст 7
Кот 6
Фотография 4
Арт 4
Отчет по обмену подарками 4
Обмен подарками 4
Тайный Санта 4
Ностальгия 3
Total tags: 296
"""
