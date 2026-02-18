import feedparser
import requests
import json
import os
from datetime import datetime

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

FEEDS = [
    "https://www.publishersweekly.com/pw/rss/index.html",
    "https://www.theguardian.com/books/rss"
]

KEYWORDS = [
    "award",
    "prize",
    "winner",
    "shortlist",
    "fellowship",
    "new novel",
    "publishing"
]

def load_posted():
    if os.path.exists("posted.json"):
        with open("posted.json", "r") as f:
            return json.load(f)
    return []

def save_posted(posted):
    with open("posted.json", "w") as f:
        json.dump(posted, f)

def contains_keyword(text):
    text = text.lower()
    return any(keyword in text for keyword in KEYWORDS)

def send_to_discord(title, link, source):
    embed = {
        "title": title,
        "url": link,
        "description": f"Source: {source}",
        "footer": {"text": "Writers Society of America — Writing News"},
        "timestamp": datetime.utcnow().isoformat()
    }

    data = {
        "embeds": [embed]
    }

    requests.post(WEBHOOK_URL, json=data)

def main():
    posted = load_posted()

    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:5]:
            combined_text = entry.title + " " + entry.get("summary", "")

            if entry.link not in posted and contains_keyword(combined_text):
                send_to_discord(entry.title, entry.link, feed.feed.title)
                posted.append(entry.link)

    save_posted(posted)

if __name__ == "__main__":
    main()
