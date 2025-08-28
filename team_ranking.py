from bs4 import BeautifulSoup

def fetch_team_rankings():
    # ranking_outerhtml.txt 파일에서 HTML 읽기
    with open("ranking_outerhtml.txt", "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    # 테이블 찾기
    table = soup.find("table", class_="Home_ranking_table__nAl-r")
    if table is None:
        raise ValueError("테이블(class='Home_ranking_table__nAl-r')을 찾을 수 없습니다.")
    tbody = table.find("tbody")
    if tbody is None:
        raise ValueError("tbody를 찾을 수 없습니다.")
    # 각 팀의 순위 행 찾기
    rows = tbody.find_all("tr", class_="Home_ranking_row__geTli")
    data = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 7:
            continue  # 데이터가 부족하면 건너뜀

        rank = cols[0].get_text(strip=True)
        team_td = cols[1]
        team_img = team_td.find("img")
        team_logo = team_img["src"] if team_img and team_img.has_attr("src") else ""
        team_name = team_img["alt"] if team_img and team_img.has_attr("alt") else ""
        games = cols[2].get_text(strip=True)
        wins = cols[3].get_text(strip=True)
        losses = cols[4].get_text(strip=True)
        draws = cols[5].get_text(strip=True)
        gb = cols[6].get_text(strip=True)

        data.append({
            "rank": rank,
            "team_name": team_name,
            "logo": team_logo,
            "games": games,
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "gb": gb
        })

    return data

# 테스트용 실행 코드
if __name__ == "__main__":
    rankings = fetch_team_rankings()
    for team in rankings:
        print(team)
