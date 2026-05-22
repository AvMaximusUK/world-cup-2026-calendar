import requests
from ics import Calendar, Event
from datetime import datetime
from zoneinfo import ZoneInfo
import uuid
import os

BST = ZoneInfo("Europe/London")

API_KEY = os.environ.get("FOOTBALL_API_KEY")

HEADERS = {"X-Auth-Token": API_KEY}

# --- FLAGS ---
FLAGS = {
    "England":"🏴󠁧󠁢󠁥󠁮󠁧󠁿","France":"🇫🇷","Brazil":"🇧🇷","Germany":"🇩🇪","Spain":"🇪🇸",
    "Argentina":"🇦🇷","USA":"🇺🇸","Mexico":"🇲🇽","Japan":"🇯🇵","Netherlands":"🇳🇱"
}

def flag(team):
    return FLAGS.get(team, "🏳️")

# --- FETCH MATCHES ---
url = "https://api.football-data.org/v4/competitions/WC/matches"
data = requests.get(url, headers=HEADERS).json()

calendar = Calendar()

for match in data.get("matches", []):

    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]

    utc_time = datetime.fromisoformat(match["utcDate"].replace("Z","+00:00"))
    bst_time = utc_time.astimezone(BST)

    title = f"{flag(home)} {home} v {flag(away)} {away}"

    stadium = match.get("venue", "World Cup Stadium")

    event = Event()
    event.name = title
    event.begin = bst_time
    event.location = stadium

    # Broadcaster not included (keeps it stable + no guessing)
    event.description = "FIFA World Cup 2026"

    event.uid = str(uuid.uuid4())

    calendar.events.add(event)

with open("worldcup.ics", "w", encoding="utf-8") as f:
    f.writelines(calendar)

print("Calendar generated")
