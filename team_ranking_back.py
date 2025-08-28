from flask import Flask, render_template, request, send_file
from team_ranking import fetch_team_rankings
import requests
from io import BytesIO

app = Flask(__name__)

@app.route("/team-ranking")
def show_ranking():
    rankings = fetch_team_rankings()
    return render_template("team_ranking.html", rankings=rankings)

@app.route("/proxy-logo")
def proxy_logo():
    url = request.args.get("url")
    if not url:
        return "Missing URL", 400
    try:
        response = requests.get(url, headers={"Referer": "https://sports.naver.com"}, timeout=5)
        if response.status_code != 200:
            return f"Image fetch failed with status {response.status_code}", 502
        return send_file(BytesIO(response.content), mimetype="image/png")
    except Exception as e:
        return f"Error fetching image: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
