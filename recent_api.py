from flask import Flask, jsonify
from flask_cors import CORS  # 추가
from recent import fetch_recent_results

app = Flask(__name__)
CORS(app)  # 이 줄을 꼭 추가!

@app.route('/api/recent/<team>')
def recent_results(team):
    results = fetch_recent_results(team)
    results += ["-"] * (5 - len(results))
    return jsonify({"team": team, "results": results})

if __name__ == "__main__":
    app.run(debug=True)
