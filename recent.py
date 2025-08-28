from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def fetch_recent_results(target_team):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    url = "https://m.sports.naver.com/kbaseball/record/kbo?seasonCode=2025&tab=teamRank"
    driver.get(url)

    try:
        # 팀 행이 로드될 때까지 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[class^='TableBody_item__']"))
        )

        team_items = driver.find_elements(By.CSS_SELECTOR, "li[class^='TableBody_item__']")

        for team in team_items:
            # 팀 이름 가져오기
            team_name_elem = team.find_element(By.CSS_SELECTOR, "div[class^='TeamInfo_team_name__']")
            team_name = team_name_elem.text.strip()

            if team_name != target_team:
                continue

            # 최근 경기 결과 (승/패/무)
            result_spans = team.find_elements(By.CSS_SELECTOR, "div.ResultInfo_result__Vd3ZN > span.blind")
            results = [span.text for span in result_spans if span.text in ["승", "패", "무"]][:5]
            return results

        return []  # 팀을 못 찾은 경우

    except Exception as e:
        print(f"❌ {target_team} 경기 결과 수집 실패:", e)
        return []

    finally:
        driver.quit()

# 테스트 실행 시 (예시)
if __name__ == "__main__":
    teams = ["한화", "LG", "롯데", "KIA", "SSG", "KT", "삼성", "NC", "두산", "키움"]
    for team in teams:
        print(f"{team}: {fetch_recent_results(team)}")
