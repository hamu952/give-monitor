import requests
import time
from bs4 import BeautifulSoup

TOKEN = "8496899351:AAHP0QR0NT95n0w_Xmr37fHKnmtaj6u4bA0"
CHAT_ID = "8350104730"

KEYWORDS = ["香水", "香氛", "小香", "coach"]

CHECK_URL = "https://www.give-circle.com/give/"

checked_ids = set()

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

def check_new_items():
    global checked_ids

    for item_id in range(1065400, 1065800):
        if item_id in checked_ids:
            continue

        url = CHECK_URL + str(item_id)
        response = requests.get(url)

        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else ""

        for kw in KEYWORDS:
            if kw in title:
                send_message(f"找到關鍵字：{kw}\n{url}")
                break

        checked_ids.add(item_id)

while True:
    check_new_items()
    time.sleep(60)
