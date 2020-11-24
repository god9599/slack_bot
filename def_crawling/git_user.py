import urllib

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# 인자로 받은 아이디의 정보를 출력한다.
def _get_user_profile(userId):
    url = "https://github.com/" + userId
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    keywords = []
    data = {}
    data['name'] = soup.find('span', class_='p-name vcard-fullname d-block overflow-hidden')
    data['bio'] = soup.find('div', class_='p-note user-profile-bio mb-3 js-user-profile-bio f4').find('div')
    data['company'] = soup.find('span', class_='p-org')
    data['location'] = soup.find('span', class_='p-label')
    data['email'] = soup.find('li', {'itemprop': 'email'})
    data['url'] = soup.find('li', {'itemprop': 'url'})

    for i, j in data.items():
        try:
            if i == 'email' or i == 'url':
                data[i] = str(j.find('a').get_text())
            else:
                data[i] = str(j.get_text())
        except:
            data[i] = 'None'

    rsffList = soup.find_all('a', class_='link-gray no-underline no-wrap')
    rsff = []
    for i in rsffList:
        try:
            ret = rsff.append(i.find('span').get_text().strip())
        except:
            break

    organizations = soup.find_all('a', class_='avatar-group-item')
    orgList = []
    for i in organizations:
        try:
            orgList.append(i.find('img')['alt'])
        except:
            break

    keywords.append("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    keywords.append("\n")
    keywords.append("\tID : " + userId)
    keywords.append("\tName : " + data['name'])
    keywords.append("\tBio : " + data['bio'])
    keywords.append("\n")
    keywords.append("\tCompany : " + data['company'])
    keywords.append("\tLocation : " + data['location'])
    keywords.append("\tEmail : " + data['email'])
    keywords.append("\tLink URL : " + data['url'])
    keywords.append("\t*Followers : " + rsff[0] + ",   Following : " + rsff[1] + ",   Stars : " + rsff[2] + "*")
    keywords.append("\n")
    keywords.append("\tOrganizations : ")
    tmp = []
    for i in orgList:
        tmp.append(i)
    keywords.append("\t\t" + str(tmp))
    keywords.append("\n")
    keywords.append("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    return u'\n'.join(keywords)


# 인자로 받은 아이디의 컨트리뷰션 그래프를 출력한다.
def _get_contributions_graph(userId):
    url = "https://github.com/" + userId
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    keywords = []
    keywords.append("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    keywords.append("\n")
    keywords.append(str(userId) + " 님의 활동 그래프 (9 번이 넘는 커밋은 *9 로 표시* 되었습니다).")
    keywords.append("\n")

    cgraph = soup.find_all('rect', class_="day")[175:]

    totalCnt = 0
    maxCnt = 0
    maxDD = ''

    for i in range(0, 7):
        rgraph = []
        cnt = i
        while cnt < len(cgraph):
            try:
                ret = int(cgraph[cnt]['data-count'])
                if maxCnt < ret:
                    maxCnt = ret
                    maxDD = cgraph[cnt]['data-date']

                totalCnt += ret

                if ret > 9:
                    ret = 9

                rgraph.append(str(ret))
            except:
                break
            cnt += 7
        keywords.append("\t" + str(rgraph))

    keywords.append("\n")
    keywords.append("\t반년간 토탈 푸쉬 횟수 : *" + str(totalCnt) + "*")
    keywords.append("\t가장 많이한 푸쉬 횟수 : *" + str(maxCnt) + "*")
    keywords.append("\t가장 많이 푸쉬한 날짜 : *" + str(maxDD) + "*")
    keywords.append("\n")
    keywords.append("\n")
    keywords.append("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    return u'\n'.join(keywords)


# yyyy/mm/dd 일에 해당하는 푸쉬 수를 출력
def _get_dd_contribution(userId, dd):
    url = "https://github.com/" + userId
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    cgraph = soup.find_all('rect', class_="day")

    ret = -1

    for i in range(len(cgraph)):
        if cgraph[i]['data-date'] == dd:
            ret = cgraph[i]['data-count']
            break

    keywords = []
    keywords.append("\n")
    if ret == -1:
        keywords.append(">\t\t날짜를 초과하셨습니다.")
    else:
        keywords.append(">\t\t" + str(userId) + " 님의 " + str(dd) + " 일 푸쉬량 : *" + str(ret) + "*")
    keywords.append("\n")

    return u'\n'.join(keywords)