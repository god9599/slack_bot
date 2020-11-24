
import urllib

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


# 크롤링 함수 구현하기
def _crawl_music_chart(text):
    # 여기에 함수를 구현해봅시다.
    url = "https://music.bugs.co.kr/chart"
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

    keywords = []

    artists = soup.find_all('p', class_='artist')

    keywords.append("*Bugs 실시간 음악 차트 Top 10*")
    keywords.append('\n')
    # for i, artist in enumerate(soup.find_all('p', class_='artist')):
    #     if i < 10:
    #         artists.append(artist.get_text().split())
    for i, keyword in enumerate(soup.find_all("p", class_="title")):
        if i < 10:
            row = "\t" + str(i + 1) + "위:  " + keyword.get_text().replace('\n', '') + " / " + str(
                artists[i].get_text().strip())
            keywords.append(row)

    keywords.append('\n')
    keywords.append('\n')
    keywords.append("*Melon 실시간 음악 차트 Top 10*")
    keywords.append('\n')

    hdr = {'User-Agent': 'Mozilla/5.0'}
    url = "https://www.melon.com/chart/index.htm"

    req = urllib.request.Request(url, headers=hdr)
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')

    artists = soup.find_all('div', class_='ellipsis rank02')

    for i, keyword in enumerate(soup.find_all("div", class_="ellipsis rank01")):
        if i < 10:
            artist = str(artists[i].get_text().strip())
            count = int(len(artist) / 2)
            artist = artist[0:count]
            row = "\t" + str(i + 1) + "위:  " + keyword.get_text().replace('\n', '') + "\t" + artist
            keywords.append(row)
            keywords.append('\n')

    # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
    return u'\n'.join(keywords)