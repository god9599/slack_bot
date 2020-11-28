import urllib
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


def serach_restaurant(text):
    baseUrl = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="
    url = baseUrl + urllib.parse.quote_plus(text + "+맛집")
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

    keywords = []

    # restaurant = soup.find_all('li', class_='list_item type_restaurant')

    # print(restaurant)

    keywords.append("=========================================")
    keywords.append("\n")
    row = ("*" + text + " 맛집*")
    keywords.append(row)
    keywords.append("\n")
    keywords.append("=========================================")
    keywords.append('\n')

    for i, keyword in enumerate(soup.find_all("li", class_="list_item type_restaurant")):
        if i < 6:
            crawl = keyword.find("a", class_="name")
            restaurant = crawl.find('span')
            menu = keyword.find('div', class_="tag_area")
            # print(menu)
            review = keyword.find('div', class_="etc_area ellp")
            link = keyword.find('a')['href']
            print(link)
            # print(review)

            keywords.append("식당 : " + restaurant.get_text())
            if (menu != None):
                keywords.append("메뉴 / 특징 : " + menu.get_text())
            keywords.append("리뷰 : " + review.get_text())
            keywords.append("링크 : " + link)
            keywords.append("==========")
            keywords.append('\n')

    # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
    return u'\n'.join(keywords)