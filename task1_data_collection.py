import os
import json
import time
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
HEADERS = {"user-agent": "TrendPulse/1.0"}

CATEGORY_KEYWORDS = {
    "technology": [
        "ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"
    ],
    "worldnews": [
        "war", "government", "country", "president", "election", "climate", "attack", "global"
    ],
    "sports": [
        "nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"
    ]
}

MAX_PER_CATEGORY = 25
FETCH_LIMIT = 500

def fetch_json(url):
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=frozenset(['GET'])
    )
    adapter = HTTPAdapter(max_retries=retry_strategy) # uses retry strategy 
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        response = session.get(url, headers=HEADERS, timeout=10) # gets the response from the url 
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Request failed for {url}: {e}")
        return None


def classify_story(title):
    title_lower = title.lower() # converts to lower case
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None


def main():
    top_story_ids = fetch_json(TOP_STORIES_URL) #gets the top stories from the hacker news
    if not top_story_ids:
        print("Could not fetch top story IDs.")
        return

    top_story_ids = top_story_ids[:FETCH_LIMIT] #assigns max limit to fetch the story Ids

    collected = {category: [] for category in CATEGORY_KEYWORDS}
    collected_ids = set()

    for category in CATEGORY_KEYWORDS:
        if len(collected[category]) >= MAX_PER_CATEGORY:
            continue

        for story_id in top_story_ids:
            if len(collected[category]) >= MAX_PER_CATEGORY:
                break

            if story_id in collected_ids:
                continue

            story = fetch_json(ITEM_URL.format(story_id))
            if not story:
                continue

            title = story.get("title", "")
            if not title:
                continue

            assigned_category = classify_story(title)
            if assigned_category != category:
                continue

            story_data = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": assigned_category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            collected[category].append(story_data) #collected story gets appended each time 
            collected_ids.add(story_id)

        time.sleep(2)

    all_stories = []
    for category in CATEGORY_KEYWORDS:
        all_stories.extend(collected[category])

    os.makedirs("data", exist_ok=True) #checks if the folder exists , if not it creates a new folder
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json" # json file is created as expected

    with open(filename, "w", encoding="utf-8") as f: # file opened in write mode
        json.dump(all_stories, f, ensure_ascii=False, indent=2)

    print(f"Collected {len(all_stories)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()
