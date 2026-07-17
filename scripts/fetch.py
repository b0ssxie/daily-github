import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")

TRANSLATE_MAX_RETRIES = 2
TRANSLATE_RETRY_DELAY = 1


def fetch_trending(date_str):
    after = f"created:>{date_str}"
    url = (
        "https://api.github.com/search/repositories"
        f"?q={after}&sort=stars&order=desc&per_page=10"
    )
    req = Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "daily-github/1.0")

    try:
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("items", [])
    except (URLError, HTTPError) as e:
        print(f"[fetch] GitHub API error: {e}", file=sys.stderr)
        return []

    projects = []
    for item in items:
        projects.append({
            "name": item.get("full_name", ""),
            "description": item.get("description") or "",
            "description_cn": "",
            "language": item.get("language") or "",
            "stars": item.get("stargazers_count", 0),
            "url": item.get("html_url", ""),
        })
    return projects


def translate_text(text):
    if not text or not text.strip():
        return ""
    try:
        from googletrans import Translator
    except ImportError:
        print("[translate] googletrans not installed, skipping translation", file=sys.stderr)
        return ""

    for attempt in range(TRANSLATE_MAX_RETRIES + 1):
        try:
            translator = Translator()
            result = translator.translate(text, src="en", dest="zh-cn")
            return result.text or ""
        except Exception as e:
            if attempt < TRANSLATE_MAX_RETRIES:
                print(f"[translate] attempt {attempt + 1} failed: {e}, retrying...", file=sys.stderr)
                time.sleep(TRANSLATE_RETRY_DELAY)
            else:
                print(f"[translate] all attempts failed: {e}", file=sys.stderr)
    return ""


def translate_projects(projects):
    for p in projects:
        if p["description"]:
            p["description_cn"] = translate_text(p["description"])


def read_index():
    path = os.path.join(DATA_DIR, "index.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"dates": []}


def write_index(dates):
    path = os.path.join(DATA_DIR, "index.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"dates": dates}, f, ensure_ascii=False, indent=2)


def main():
    today_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"[fetch] fetching trending repos for date: {today_utc}")

    projects = fetch_trending(today_utc)
    print(f"[fetch] got {len(projects)} projects")

    translate_projects(projects)

    day_file = os.path.join(DATA_DIR, f"{today_utc}.json")
    with open(day_file, "w", encoding="utf-8") as f:
        json.dump({"date": today_utc, "projects": projects}, f, ensure_ascii=False, indent=2)
    print(f"[fetch] wrote {day_file}")

    index = read_index()
    dates = index.get("dates", [])
    if today_utc not in dates:
        dates.insert(0, today_utc)
        dates.sort(reverse=True)
        write_index(dates)
        print(f"[fetch] updated index.json with {today_utc}")
    else:
        print(f"[fetch] {today_utc} already in index, skipping index update")


if __name__ == "__main__":
    main()