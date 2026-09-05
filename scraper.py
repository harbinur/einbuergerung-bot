import requests
from bs4 import BeautifulSoup
import re
import os

URL = "https://www.dresden.de/de/rathaus/dienstleistungen/einbuergerung_d115.php"
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
STATE_FILE = "last_value.txt"

def get_value():
    r = requests.get(URL, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(separator="\n")

    match = re.search(r"Aktuelle Bearbeitung:\s*Anträge aus\s*([A-Za-zÄÖÜäöü]+\s*\d{4})", text)
    return match.group(1).strip() if match else None

def read_last_value():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def write_last_value(value):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(value)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

value = get_value()
last_value = read_last_value()

if value is None:
    send_telegram("Aylık güncelleme: 'Anträge aus' bilgisi bulunamadı")
elif value != last_value:
    send_telegram(f"🔔 Einbürgerung durumu güncellendi!\nŞu an işlenen başvurular → {value}")
    write_last_value(value)
else:
    print(f"Değişiklik yok, hala: {value}")
