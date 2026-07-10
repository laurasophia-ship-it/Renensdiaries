import requests
import random
from datetime import date
import xml.etree.ElementTree as ET

NTFY_SERVER = "https://ntfy.sh"
NTFY_TOPIC = "Renensdiaries"  # ton canal de diffusion

# Coordonnées de Renens (pour le coucher du soleil)
RENENS_LAT = 46.5399
RENENS_LNG = 6.5881


def get_sunset_time():
    url = "https://api.sunrise-sunset.org/json"
    params = {
        "lat": RENENS_LAT,
        "lng": RENENS_LNG,
        "date": "today",
        "formatted": 0,
        "tzid": "Europe/Zurich",
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()["results"]["sunset"]
    sunset_time = data.split("T")[1][:5]
    return sunset_time


def get_swiss_sport_news():
    url = "https://www.swissinfo.ch/service/rss/sport"
    resp = requests.get(url)
    resp.raise_for_status()

    root = ET.fromstring(resp.content)
    items = root.findall(".//item")

    news_lines = ["🏅 Sport en Suisse (Swissinfo) :"]

    for item in items[:3]:
        title = item.find("title").text
        news_lines.append(f"• {title} 💫")

    return "\n".join(news_lines)


def get_aquarius_horoscope():
    return "♒ Horoscope Verseau : aujourd’hui, fais confiance à ton intuition ✨"


def get_cute_animal_emoji():
    emojis = ["🐶", "🐱", "🐰", "🐹", "🦊", "🐻", "🐼", "🐨", "🐸", "🐥"]
    return random.choice(emojis)


def get_cute_phrase():
    phrases = [
        "Tu as fait de ton mieux aujourd’hui, et c’est déjà trop mignon 🐥",
        "Même les petits pas comptent, et tu en as fait plein ✨",
        "Tu mérites un câlin imaginaire, juste parce que tu es toi 🐻",
        "Aujourd’hui tu as été adorable, même si tu ne t’en rends pas compte 💛",
        "Tu fais fondre le monde un petit peu chaque jour 🌼",
    ]
    return random.choice(phrases)


def build_message():
    today = date.today().strftime("%d.%m.%Y")
    sunset = get_sunset_time()
    sport = get_swiss_sport_news()
    horoscope = get_aquarius_horoscope()
    animal = get_cute_animal_emoji()
    cute_phrase = get_cute_phrase()

    lines = [
        "bravo Dudu la journée est finie ! ✨",
        f"📅 Date : {today}",
        f"🌇 Coucher de soleil à Renens : {sunset}",
        "",
        sport,
        "",
        horoscope,
        "",
        f"💛 Phrase cute du jour : {cute_phrase}",
        "",
        f"🐾 Animal mignon du jour : {animal}",
    ]

    return "\n".join(lines)


def send_to_ntfy(message: str):
    url = f"{NTFY_SERVER.rstrip('/')}/{NTFY_TOPIC}"
    headers = {
        "Title": "Renens Diaries",
        "Tags": "sunset,horoscope,sport"
    }
    resp = requests.post(url, data=message.encode("utf-8"), headers=headers)
    resp.raise_for_status()
    print(f"Message envoyé sur {url} (status {resp.status_code})")


if __name__ == "__main__":
    msg = build_message()
    print("Message généré :")
    print(msg)
    send_to_ntfy(msg)
