from recent import fetch_recent_results  # ✅ 크롤링 함수

teams = ["한화", "LG", "롯데", "KIA", "SSG", "KT", "삼성", "NC", "두산", "키움"]

def main():
    for team in teams:
        try:
            results = fetch_recent_results(team)
        except Exception as e:
            print(f"❌ {team} 에러 발생: {e}")
            results = ["-"] * 5

        # 5경기 안 될 경우 '-'로 채움
        results += ["-"] * (5 - len(results))

        print(f"{team}: {' | '.join(results)}")

if __name__ == "__main__":
    main()
