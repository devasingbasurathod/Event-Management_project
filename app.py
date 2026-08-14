import json
import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DATA_FILE = "events.json"


def load_events():
  if not os.path.exists(DATA_FILE):
    return []
  with open(DATA_FILE, "r") as f:
    try:
      return json.load(f)
    except json.JSONDecodeError:
      return []


def save_events(events):
  with open(DATA_FILE, "w") as f:
    json.dump(events, f, indent=2)


@app.route("/")
def index():
  events = load_events()
  return render_template("index.html", events=events)


@app.route("/api/events", methods=["GET", "POST"])
def handle_events():
  events = load_events()

  if request.method == "POST":
    data = request.get_json()
    new_event = {
        "id": len(events) + 1,
        "title": data.get("title"),
        "date": data.get("date"),
        "category": data.get("category"),
        "location": data.get("location"),
        "description": data.get("description"),
    }
    events.append(new_event)
    save_events(events)
    return jsonify({"success": True, "event": new_event}), 201

  return jsonify(events)


if __name__ == "__main__":
  app.run(debug=True, port=5000)