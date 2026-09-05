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
    text = soup.get_text(separator="\n")

    wartezeit = re.search(r"Aktuelle Wartezeit ab Antragstellung:\s*([^\n]+)", text)
    bearbeitung = re.search(r"Aktuelle Bearbeitung:\s*([^\n]+)", text)

    wartezeit_val = wartezeit.group(1).strip() if wartezeit else None
    bearbeitung_val = bearbeitung.group(1).strip() if bearbeitung else None

    return wartezeit_val, bearbeitung_val

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

wartezeit, bearbeitung = get_value()
if wartezeit:
    msg = f"Aylık Einbürgerung güncellemesi:\nWartezeit: {wartezeit}"
    if bearbeitung:
        msg += f"\nBearbeitung: {bearbeitung}"
    send_telegram(msg)
else:
    send_telegram("Aylık güncelleme: değer bulunamadı")
