# AGENTS.md — 开源日报

## Project overview

A fully automated "daily open-source news" static site on GitHub Pages. GitHub Actions fetches trending repos daily via the GitHub Search API, translates descriptions to Chinese, and commits the data. The frontend is a single `index.html` with inline CSS/JS.

- **Stack**: HTML/CSS/JS (zero deps) + Python 3 (stdlib + `googletrans`) + GitHub Actions + GitHub Pages
- **No build step, no bundler, no package.json, no test framework.**

## Architecture & data flow

```
index.html  (served by GitHub Pages)
  └─ fetches data/index.json  →  date sidebar
  └─ fetches data/{date}.json  →  project cards

scripts/fetch.py  (run by .github/workflows/daily.yml)
  ├─ GitHub Search API  →  trending repos (past 7 days, top 10 by most stars)
  ├─ deep-translator    →  EN → zh-CN translation
  ├─ writes data/{today}.json
  └─ updates data/index.json
```

## Data format

- `data/index.json`: `{"dates": ["2026-07-17", ...]}` — sorted descending.
- `data/YYYY-MM-DD.json`: `{"date": "...", "projects": [{"name", "description", "description_cn", "language", "stars", "url"}]}` — up to 10 items.

## Commands

- **Fetch data locally (one-shot):**
  ```
  pip install deep-translator
  python scripts/fetch.py
  ```
  Requires `GITHUB_TOKEN` env var (optional; unauthenticated works within rate limits).

- **Manual CI trigger:** Go to Actions → "Daily Update" → Run workflow.

- **No build, test, or lint commands exist** for this repo.

## CI (`.github/workflows/daily.yml`)

- Cron: `0 0 * * *` UTC (Beijing 08:00).
- Workflow needs **Contents: write** permission (auto-commits `data/` back to repo).
- Only adding/modifying files under `data/` — never touches frontend code.

## Translation gotchas

- `deep-translator` pinned in the workflow. The library can fail silently with network errors; the script handles retry (2 attempts) and leaves `description_cn` empty on failure rather than crashing.
- Translation is best-effort — check `description_cn` presence before displaying.

## Frontend quirks

- Theme preference persisted in `localStorage` key `daily_github_theme`.
- Dark/light CSS lives in `[data-theme="dark"]` / `:root` custom properties.
- `escapeHtml` uses DOM node creation (not a library) — safe for user content.
- All state is in-closure (IIFE in `<script>`); no global pollution beyond DOM IDs.

## Existing docs

- `docs/superpowers/specs/2026-07-17-daily-github-design.md` — full design spec with data format, layout, error handling, and user setup instructions. Read this before major changes.