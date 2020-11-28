from urllib.request import urlopen, Request
import urllib
import bs4


def search_weather(location):
    Finallocation = urllib.parse.quote(location + '+날씨')
    LocationInfo = ""
    NowTemp = ""
    CheckDust = []
    url = 'https://search.naver.com/search.naver?ie=utf8&query=' + Finallocation
    hdr = {'User-Agent': (
        'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/86.0.4240.198 safari/537.36')}
    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, 'html5lib')

    keywords = []

    # 오류 체크
    ErrorCheck = soup.find('span', {'class': 'btn_select'})

    if 'None' in str(ErrorCheck):
        row = "위치를 다시 검색해주세용~~"
        keywords.append(row)

        return u'\n'.join(keywords)

    else:
        # 지역 정보
        for i in soup.select('span[class=btn_select]'):
            LocationInfo = i.text

        # 현재 온도
        NowTemp = soup.find('span', {'class': 'todaytemp'}).text + soup.find('span', {'class': 'tempmark'}).text[2:]

        # 날씨 캐스트
        WeatherCast = soup.find('p', {'class': 'cast_txt'}).text

        # 오늘 오전온도, 오후온도, 체감온도
        TodayMorningTemp = soup.find('span', {'class': 'min'}).text
        TodayAfternoonTemp = soup.find('span', {'class': 'max'}).text
        TodayFeelTemp = soup.find('span', {'class': 'sensible'}).text[5:]

        # 자외선 지수
        TodayUV = soup.find('span', {'class': 'indicator'}).text[4:-2] + " " + soup.find('span',
                                                                                         {'class': 'indicator'}).text[
                                                                               -2:]

        # 미세먼지, 초미세먼지, 오존 지수
        CheckDust1 = soup.find('div', {'class': 'sub_info'})
        CheckDust2 = CheckDust1.find('div', {'class': 'detail_box'})
        for i in CheckDust2.select('dd'):
            CheckDust.append(i.text)
        FineDust = CheckDust[0][:-2] + " " + CheckDust[0][-2:]
        UltraFineDust = CheckDust[1][:-2] + " " + CheckDust[1][-2:]
        Ozon = CheckDust[2][:-2] + " " + CheckDust[2][-2:]

        # 내일 오전, 오후 온도 및 상태 체크
        tomorrowArea = soup.find('div', {'class': 'tomorrow_area'})
        tomorrowCheck = tomorrowArea.find_all('div', {'class': 'main_info morning_box'})

        # 내일 오전온도
        tomorrowMoring1 = tomorrowCheck[0].find('span', {'class': 'todaytemp'}).text
        tomorrowMoring2 = tomorrowCheck[0].find('span', {'class': 'tempmark'}).text[2:]
        tomorrowMoring = tomorrowMoring1 + tomorrowMoring2

        # 내일 오전상태
        tomorrowMState1 = tomorrowCheck[0].find('div', {'class': 'info_data'})
        tomorrowMState2 = tomorrowMState1.find('ul', {'class': 'info_list'})
        tomorrowMState3 = tomorrowMState2.find('p', {'class': 'cast_txt'}).text
        tomorrowMState4 = tomorrowMState2.find('div', {'class': 'detail_box'})
        tomorrowMState5 = tomorrowMState4.find('span').text.strip()
        tomorrowMState = tomorrowMState3 + " " + tomorrowMState5

        # 내일 오후온도
        tomorrowAfter1 = tomorrowCheck[1].find('p', {'class': 'info_temperature'})
        tomorrowAfter2 = tomorrowAfter1.find('span', {'class': 'todaytemp'}).text
        tomorrowAfter3 = tomorrowAfter1.find('span', {'class': 'tempmark'}).text[2:]
        tomorrowAfter = tomorrowAfter2 + tomorrowAfter3

        # 내일 오후상태
        tomorrowAState1 = tomorrowCheck[1].find('div', {'class': 'info_data'})
        tomorrowAState2 = tomorrowAState1.find('ul', {'class': 'info_list'})
        tomorrowAState3 = tomorrowAState2.find('p', {'class': 'cast_txt'}).text
        tomorrowAState4 = tomorrowAState2.find('div', {'class': 'detail_box'})
        tomorrowAState5 = tomorrowAState4.find('span').text.strip()
        tomorrowAState = tomorrowAState3 + " " + tomorrowAState5


        keywords.append("=========================================")
        keywords.append("\n")
        row = (LocationInfo + " 날씨 정보입니다.")
        keywords.append(row)
        keywords.append("\n")
        keywords.append("=========================================")
        row = ("현재온도: " + NowTemp)
        keywords.append(row)
        row = ("체감온도: " + TodayFeelTemp)
        keywords.append(row)
        row = ("오전/오후 온도: " + TodayMorningTemp + "/" + TodayAfternoonTemp)
        keywords.append(row)
        row = ("현재 상태: " + WeatherCast)
        keywords.append(row)
        row = ("현재 자외선 지수: " + TodayUV)
        keywords.append(row)
        row = ("현재 미세먼지 농도: " + FineDust)
        keywords.append(row)
        row = ("현재 초미세먼지 농도: " + UltraFineDust)
        keywords.append(row)
        row = ("현재 오존 지수: " + Ozon)
        keywords.append(row)
        keywords.append("=========================================")
        keywords.append("\n")
        row = (LocationInfo + " 내일 날씨 정보입니다.")
        keywords.append(row)
        keywords.append("=========================================")
        keywords.append("\n")
        row = ("내일 오전 온도: " + tomorrowMoring)
        keywords.append(row)
        row = ("내일 오전 상태: " + tomorrowMState)
        keywords.append(row)
        row = ("내일 오후 온도: " + tomorrowAfter)
        keywords.append(row)
        row = ("내일 오후 상태: " + tomorrowAState)
        keywords.append(row)
        keywords.append('\n')
        keywords.append('\n')

        # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
        return u'\n'.join(keywords)