import requests
import random
from datetime import date

NTFY_SERVER = "https://ntfy.sh"
NTFY_TOPIC = "Renensdiaries"  # ton canal de diffusion

# Coordonnées de Renens (pour le coucher du soleil)
RENENS_LAT = 46.5399
RENENS_LNG = 6.5881


def get_sunset_time():
    """
    Récupère l'heure du coucher de soleil à Renens pour aujourd'hui
    via une API publique.
    """
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
    # Exemple: "2026-07-07T19:22:59+00:00" → on garde juste l'heure
    sunset_time = data.split("T")[1][:5]
    return sunset_time


def get_swiss_sport_news():
    """
    TODO: ici on pourrait aller chercher les actus sport suisses
    (par ex. télétext ou site sportif).
    Pour l'instant, on met un texte fixe.
    """
    return "🏅 Sport en Suisse : résultats et actus du jour (à compléter)."


def get_aquarius_horoscope():
    """
    TODO: aller chercher l’horoscope Verseau sur le site LFM.
    Pour l’instant, texte fixe.
    """
    return "♒ Horoscope Verseau LFM : aujourd’hui, fais confiance à ton intuition."


def get_cute_animal_emoji():
    emojis = ["🐶", "🐱", "🐰", "🐹", "🦊", "🐻", "🐼", "🐨", "🐸", "🐥"]
    return random.choice(emojis)


def get_ai_text():
    """
    Texte 'créé par l’IA'.
    Plus tard, tu pourras le remplacer par un vrai appel à une API d’IA.
    """
    return "Petit texte inspirant du jour : tu as fait de ton mieux, et c’est déjà énorme."


def build_message():
    today = date.today().strftime("%d.%m.%Y")
    sunset = get_sunset_time()
    sport = get_swiss_sport_news()
    horoscope = get_aquarius_horoscope()
    animal = get_cute_animal_emoji()
    ai_text = get_ai_text()

    lines = [
        "bravo Dudu la journée est finie !",
        f"📅 Date : {today}",
        f"🌇 Coucher de soleil à Renens : {sunset}",
        "",
        sport,
        "",
        horoscope,
        "",
        ai_text,
        "",
        f"Animal mignon du jour : {animal}",
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
