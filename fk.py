import requests
import json
import re
from datetime import datetime

url = "https://api-gw.sports.naver.com/cms/templates/kbaseball_new_home_feed"
headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)
data = res.json()

broadcasts = []

def is_score_or_vs(title):
    return bool(re.search(r'\d+\s*:\s*\d+', title)) or "vs" in title

today = datetime.now().strftime("%Y-%m-%d")

for template in data.get("result", {}).get("templates", []):
    if template.get("templateId") == "new_today_match_template":
        schedules = template.get("json", {}).get("schedulesBySection", {}).get("kbaseballetc", {}).get("schedules", [])
        for item in schedules:
            game_date = item.get("gameStartTime", "")[:10]
            if game_date == today and not is_score_or_vs(item.get("title", "")):
                broadcasts.append({
                    "title": item.get("title"),
                    "url": item.get("landingUrl", ""),
                    "mainImage": item.get("liveInfo", {}).get("images", [None])[0],
                    "gameStartTime": item.get("gameStartTime", ""),
                    "statusInfo": item.get("statusInfo", "")
                })

with open("../src/broadcast_schedule.json", "w", encoding="utf-8") as f:
    json.dump(broadcasts, f, ensure_ascii=False, indent=2)

print("야구 기타 오늘 방송/예정 항목 개수:", len(broadcasts))
for b in broadcasts:
    print(b["title"])
