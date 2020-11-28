from bs4 import BeautifulSoup
import requests


def _crawl_naver_search():
    json = requests.get('https://www.naver.com/srchrank?frm=main').json()

    ranks = json.get("data")
    keywords = []

    keywords.append("*네이버 실시간 검색어*")
    keywords.append('\n')
    keywords.append("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    for key in ranks:
        rank = key.get("rank")
        keyword = key.get("keyword")
        row = "\t" + str(rank) + "위:  " + keyword
        keywords.append(row)

    keywords.append("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
    return u'\n'.join(keywords)
