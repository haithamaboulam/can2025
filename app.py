from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "6d837a8c286c507b1947ddf61099f11f"  # Ta clé API
LEAGUE_ID = 61   # Ligue 1 France pour test
SEASON = 2023    # Saison 2023

@app.route("/scores")
def get_scores():
    url = f"https://v3.football.api-sports.io/fixtures?league={LEAGUE_ID}&season={SEASON}"
    headers = {"x-apisports-key": API_KEY}

    response = requests.get(url, headers=headers)
    data = response.json()

    matches = []
    for match in data.get("response", []):
        matches.append({
            "teams": {
                "home": {"name": match["teams"]["home"]["name"]},
                "away": {"name": match["teams"]["away"]["name"]}
            },
            "goals": {
                "home": match["goals"]["home"] if match["goals"]["home"] is not None else 0,
                "away": match["goals"]["away"] if match["goals"]["away"] is not None else 0
            },
            "fixture": {
                "status": {
                    "elapsed": match["fixture"]["status"]["elapsed"] if match["fixture"]["status"]["elapsed"] else 0
                },
                "date": match["fixture"]["date"]
            }
        })

    return jsonify({"response": matches})

if __name__ == "__main__":
    print("Serveur Flask démarré ! Accédez à http://127.0.0.1:5000/scores")
    app.run(debug=True)
