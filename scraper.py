import requests
from bs4 import BeautifulSoup
import re
import os

URL = "https://www.dresden.de/de/rathaus/dienstleistungen/einbuergerung_d115.php"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_value():
    r = requests.get(URL, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text()

    match = re.search(r"(\d+)\s*Monat", text, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

value = get_value()
if value:
    send_telegram(f"Aylık Einbürgerung güncellemesi: Wartezeit {value} ay")
else:
    send_telegram("Aylık güncelleme: sayı bulunamadı")
