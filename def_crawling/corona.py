
import urllib

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


def _crawl_corona():
    url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98'
    hdr = {'User-Agent': 'Mozilla/5.0'}

    req = Request(url, headers=hdr)
    html = urllib.request.urlopen(req)
    # bsObj = BeautifulSoup.BeautifulSoup(html, "html.parser")
    bsObj = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

    keywords = []

    # 확진환자

    ncov1 = bsObj.find('li', {'class': 'info_01'})
    ncov2 = ncov1.find('p', {'class': 'info_num'})
    ncov3 = ncov1.find('em', {'class': 'info_variation'})
    ncovp1 = ncov2.text.strip()
    ncovp11 = ncov3.text.strip()

    # 격리해체

    ncov4 = bsObj.find('li', {'class': 'info_02'})
    ncov5 = ncov4.find('p', {'class': 'info_num'})
    ncov6 = ncov4.find('em', {'class': 'info_variation'})
    ncovp2 = ncov5.text.strip()
    ncovp22 = ncov6.text.strip()

    # 검사중

    ncov7 = bsObj.find('li', {'class': 'info_03'})
    ncov8 = ncov7.find('p', {'class': 'info_num'})
    ncov9 = ncov7.find('em', {'class': 'info_variation'})
    ncovp3 = ncov8.text.strip()
    ncovp33 = ncov9.text.strip()

    # 사망자

    ncov10 = bsObj.find('li', {'class': 'info_04'})
    ncov11 = ncov10.find('p', {'class': 'info_num'})
    ncov12 = ncov10.find('em', {'class': 'info_variation'})
    ncovp4 = ncov11.text.strip()
    ncovp44 = ncov12.text.strip()

    a = '　확진자: '
    b = '　격리해제: '
    c = '　검사대기: '
    d = '　사망자: '
    e = '명'

    keywords.append("*실시간 국내 코로나 현황*")
    keywords.append('\n')
    row = (a + ncovp1 + e + '\t' + ncovp11 + " ▲")
    keywords.append(row)
    row = (b + ncovp2 + e + '\t' + ncovp22 + " ▲")
    keywords.append(row)
    row = (c + ncovp3 + e + '\t' + ncovp33 + " ▲")
    keywords.append(row)
    row = (d + ncovp4 + e + '\t\t' + ncovp44 + " ▲")
    keywords.append(row)
    keywords.append('\n')
    keywords.append('\n')

    # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
    return u'\n'.join(keywords)