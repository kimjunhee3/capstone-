import requests
import json

url = "https://api-gw.sports.naver.com/cms/contents/adContents/KBASEBALL?multiContents=Y"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

res = requests.get(url, headers=headers)
data = res.json()

banners = []
# adAccounts로 수정
if "result" in data and "adAccounts" in data["result"]:
    for ad in data["result"]["adAccounts"]:
        for ad_content in ad.get("adContents", []):
            contents = ad_content.get("contents", {})
            # 왼쪽 배너
            if contents.get("leftSideImage") and contents.get("leftUrl"):
                banners.append({
                    "image": contents["leftSideImage"],
                    "link": contents["leftUrl"]
                })
            # 오른쪽 배너
            if contents.get("rightSideImage") and contents.get("rightUrl"):
                banners.append({
                    "image": contents["rightSideImage"],
                    "link": contents["rightUrl"]
                })

    with open("today_banner.json", "w", encoding="utf-8") as f:
        json.dump(banners, f, ensure_ascii=False, indent=2)
    print("배너 개수:", len(banners))
else:
    print("result 또는 adAccounts 키가 없습니다. 응답 구조를 다시 확인해 주세요.")
