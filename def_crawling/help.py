
# Help desk
def _help_desk():
    keywords = []
    keywords.append("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    keywords.append("\n")
    keywords.append("HELP:: 명령어 리스트.")
    keywords.append("\n")
    keywords.append("\t1. *music* : 벅스와 멜론에서 각각 인기순위 탑 10을 출력합니다.")
    keywords.append("\n")
    keywords.append("\t2. *corona* : 현재 날짜의 국내 코로나 현황을 출력합니다.")
    keywords.append("\n")
    keywords.append("\t3. *weather* : 현재 날짜의 날씨를 출력합니다.")
    keywords.append("\n")
    keywords.append("\t4. *{아이디}*, *{행동1}* : 각 { } 안에 명령어를 넣어주세요.")
    keywords.append("\t\t\t{아이디}, 0 : 해당 아이디의 정보를 출력합니다.")
    keywords.append("\t\t\t{아이디}, 1 : 해당 아이디의 반 년간 푸쉬량을 그래프로 보여줍니다.")
    keywords.append("\t\t\t{아이디}, yyyy-mm-dd : yyyy-mm-dd 일에 푸쉬한 횟수를 출력합니다.")
    keywords.append('\n')
    keywords.append("\t5. *boj, {문제분류}, {난이도}* : 백준에서 문제분류에 해당하는 난이도를 가져옵니다.")
    keywords.append("\t\t\t난이도 : 0 - easy, 1 - middle, 2 - hard, *random* - 무작위")
    keywords.append("\t\t\t문제분류 : dp, bfs, dfs, brute, 다익스트라, 분할정복, graph-basic, graph,")
    keywords.append("\t\t\t\t\t구현, 문자열, 수학, 순열, 조합, 정렬, 탐색, 자료구조, 백트래킹, 스택, 큐, 덱, 해싱")
    keywords.append("\t\t\t_e.x) boj, bfs, 0 : bfs 쉬운 문제들을 가져옵니다._")
    keywords.append('\n')
    keywords.append("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

    return u'\n'.join(keywords)