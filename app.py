from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data.json'

FRIENDS = ["Jones", "Matthi", "Staels", "Coppens", "Dyldo", "Brem"]

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"sightings": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_sjwans_status(days_since):
    if days_since is None:
        return {"emoji": "❓", "text": "Niemand weet waar Sjwans is...", "img": "sjwans4.png"}
    elif days_since < 3:
        return {"emoji": "😎", "text": "Vers gespot op café. De legende leeft!", "img": "sjwans1.png"}
    elif days_since < 14:
        return {"emoji": "🕵️‍♂️", "text": "Hij is ondergedoken. Vermoedelijk bij Matthi thuis.", "img": "sjwans2.png"}
    elif days_since < 30:
        return {"emoji": "🧙‍♂️", "text": "Er is slechts één foto in slechte kwaliteit opgedoken.", "img": "sjwans3.png"}
    else:
        return {"emoji": "👻", "text": "Niemand heeft hem al weken gezien. Bestaat hij nog?", "img": "sjwans4.png"}

@app.route('/')
def index():
    data = load_data()
    sightings = data.get("sightings", [])
    if sightings:
        last_sighting = sightings[-1]
        last_date = datetime.strptime(last_sighting["date"], "%Y-%m-%d")
        days_since = (datetime.now() - last_date).days
    else:
        last_sighting = None
        days_since = None

    status = get_sjwans_status(days_since)

    leaderboard = {}
    for s in sightings:
        leaderboard[s["name"]] = leaderboard.get(s["name"], 0) + 1
    leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)

    return render_template(
        "index.html",
        last_sighting=last_sighting,
        days_since=days_since,
        status=status,
        sightings=sightings[::-1],
        leaderboard=leaderboard
    )

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        data = load_data()
        data["sightings"].append({"name": name, "date": date})
        save_data(data)
        return redirect(url_for('index'))
    return render_template("update.html", friends=FRIENDS)

if __name__ == '__main__':
    app.run(debug=True)
