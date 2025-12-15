import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

TOKEN = "8496899351:AAHP0QR0NT95n0w_Xmr37fHKnmtaj6u4bA0"
CHAT_ID = "8350104730"

KEYWORDS = ["香水", "香氛", "小香", "coach"]

BASE_URL = "https://www.give-circle.com/give/"
START_ID = 1065459      # 已知存在的 ID
CHECK_RANGE = 40        # 往回檢查筆數

# 用來避免同一分鐘內重複通知
notified_urls = set()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def scan_once(tag):
    found_any = False
    for item_id in range(START_ID, START_ID - CHECK_RANGE, -1):
        url = BASE_URL + str(item_id)
        if url in notified_urls:
            continue

        try:
            r = requests.get(url, timeout=10)
        except requests.RequestException:
            continue

        if r.status_code != 200:
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string if soup.title else ""
        text = soup.get_text()
        content = (title + text).lower()

        for kw in KEYWORDS:
            if kw.lower() in content:
                send_telegram(
                    f"🎁【30秒監控-{tag}】發現關鍵字【{kw}】\n{url}"
                )
                notified_urls.add(url)
                found_any = True
                break
    return found_any

def main():
    # 第一次掃描（T=0s）
    scan_once("第1次")

    # 等 30 秒
    time.sleep(30)

    # 第二次掃描（T=30s）
    scan_once("第2次")

if __name__ == "__main__":
    main()
send_telegram("✅ 測試通知：Give 監控系統已成功運作")
