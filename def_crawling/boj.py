import urllib

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# BOJ 문제 크롤링
def _get_boj(tag, level):
    def getRatio(e):
        return float(e[5])

    if tag == 'dp':
        tag = '25'
    elif tag == 'graph-basic':
        tag = '7'
    elif tag == 'graph':
        tag = '11'
    elif tag == '다익스트라':
        tag = '22'
    elif tag == '분할정복':
        tag = '24'
    elif tag == 'brute':
        tag = '125'
    elif tag == '문자열':
        tag = '158'

    # url = "https://www.acmicpc.net/problem/tag/" + urllib.parse.quote(tag)
    url = "https://www.acmicpc.net/problemset?sort=ac_desc&algo=" + tag
    pUrl = "https://www.acmicpc.net"
    keywords = []

    try:
        req = urllib.request.Request(url, headers=hds)
        soup = BeautifulSoup(urllib.request.urlopen(req).read(), "html.parser")

        problem_list = soup.find_all('tr')[1:]
        pp_list = []
        pp = []

        for e in problem_list:
            pp_list.append(e.find_all('td'))

        for e in pp_list:
            tmp = []
            for i in range(len(e)):
                if i == 1:
                    tmp.append(e[i])
                elif i == 5:
                    tmp.append(e[i].get_text()[0:5])
                else:
                    tmp.append(e[i].get_text())
            pp.append(tmp)
        pp = sorted(pp, key=getRatio, reverse=True)

        if level == 'random':
            rn = random.randint(0, len(pp) - 1)
            keywords.append(pp[rn][0] + "번 *[" + pp[rn][1].get_text() + "]* \t\t정답 비율: " + pp[rn][5])
            keywords.append(pUrl + pp[rn][1].find('a')['href'])
        else:
            for e in pp:
                if level == '0' and float(e[5]) >= 60:
                    keywords.append(e[0] + "번 *[" + e[1].get_text() + "]* \t\t정답 비율: " + e[5])
                    keywords.append(pUrl + e[1].find('a')['href'])

                elif level == '1' and 30 < float(e[5]) < 60:
                    keywords.append(e[0] + "번 *[" + e[1].get_text() + "]* 정답 비율: " + e[5])
                    keywords.append(pUrl + e[1].find('a')['href'])
                elif level == '2' and -1 < float(e[5]) < 30:
                    keywords.append(e[0] + "번 *[" + e[1].get_text() + "]* 정답 비율: " + e[5])
                    keywords.append(pUrl + e[1].find('a')['href'])
                if len(keywords) > 10:
                    break

    except:
        keywords.append("찾을 수 없습니다. 인자를 확인해 주세요.")

    return u'\n'.join(keywords)