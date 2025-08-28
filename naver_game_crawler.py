import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def crawl_preview(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 투수 정보 추출
    pitchers = []
    pitcher_boxes = soup.select('.PreviewPitcherInfo_pitcher__2ve9Q')  # 실제 클래스 확인 필요
    pitcher_names = [el.get_text(strip=True) for el in soup.select('.PreviewPitcherInfo_name__1wRjE')]
    pitcher_stats = soup.select('.PreviewPitcherInfo_table__1c7ZV tr')
    pitcher_info = []
    for tr in pitcher_stats:
        tds = tr.select('td')
        if len(tds) == 3:
            pitcher_info.append({
                "left": tds[0].get_text(strip=True),
                "label": tds[1].get_text(strip=True),
                "right": tds[2].get_text(strip=True)
            })

    # 주요 구종
    pitch_types = []
    for box in soup.select('.PreviewPitcherInfo_barchart__3X2Jl'):
        pitch_list = []
        for item in box.select('.PreviewPitcherInfo_item__2nQpK'):
            pitch_type = item.select_one('.PreviewPitcherInfo_type__3c2Ol').get_text(strip=True)
            pitch_speed = item.select_one('.PreviewPitcherInfo_speed__2nJzC').get_text(strip=True) if item.select_one('.PreviewPitcherInfo_speed__2nJzC') else ''
            pitch_rate = item.select_one('.PreviewPitcherInfo_rate__2CwLz').get_text(strip=True)
            pitch_list.append({
                "type": pitch_type,
                "speed": pitch_speed,
                "rate": pitch_rate
            })
        pitch_types.append(pitch_list)

    # 키플레이어 정보
    batter_names = [el.get_text(strip=True) for el in soup.select('.PreviewBatterInfo_name__1wRjE')]
    batter_stats = soup.select('.PreviewBatterInfo_table__1c7ZV tr')
    batter_info = []
    for tr in batter_stats:
        tds = tr.select('td')
        if len(tds) == 3:
            batter_info.append({
                "left": tds[0].get_text(strip=True),
                "label": tds[1].get_text(strip=True),
                "right": tds[2].get_text(strip=True)
            })

    # HOT & COLD ZONE
    hot_cold = []
    for zone in soup.select('.PreviewBatterInfo_hotcold__2a4R2'):
        squares = [el.get_text(strip=True) for el in zone.select('.PreviewBatterInfo_square__1qPCA')]
        hot_cold.append(squares)

    driver.quit()
    return {
        "pitcher_names": pitcher_names,
        "pitcher_info": pitcher_info,
        "pitch_types": pitch_types,
        "batter_names": batter_names,
        "batter_info": batter_info,
        "hot_cold": hot_cold,
    }
