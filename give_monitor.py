import requests
from bs4 import BeautifulSoup
import os

# ===== 監控設定 =====
SEARCH_URL = "https://www.give-circle.com/search?keyword="
KEYWORDS = ["香水", "香氛", "小香", "coach", "jo malone"]

BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
CHAT_ID = os.environ.get("TG_CHAT_ID")

SEEN_FILE = "seen.txt"


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": False
    }
    requests.post(url, data=payload)


def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f.readlines())


def save_seen(seen):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        for link in sorted(seen):
            f.write(link + "\n")


def main():
    seen = load_seen()
    headers = {"User-Agent": "Mozilla/5.0"}
    found_links = set()

    for kw in KEYWORDS:
        url = SEARCH_URL + kw
        res = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(res.text, "html.parser")

        for a in soup.select("a[href^='/give/']"):
            title = a.get_text(strip=True)
            href = a["href"]
            title_lower = title.lower()

            if kw.lower() in title_lower:
                full_url = "https://www.give-circle.com" + href
                found_links.add(full_url)

    new_links = found_links - seen

    for link in new_links:
        send_telegram(f"🎁 發現新的關鍵字贈物：\n{link}")

    if new_links:
        seen.update(new_links)
        save_seen(seen)


if __name__ == "__main__":
    main()
