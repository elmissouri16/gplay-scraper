# Examples

Practical recipes that showcase how to use GPlay Scraper in real projects.

## Basic App Information

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
app_id = "com.whatsapp"

basic_info = scraper.app_get_fields(
    app_id,
    ["title", "developer", "genre", "score", "free"],
    lang="en",
    country="us",
)

media_info = scraper.app_get_fields(
    app_id,
    ["icon", "screenshots", "headerImage"],
    assets="LARGE",  # 2048px images
)

for field, value in basic_info.items():
    print(f"{field}: {value}")
```

Output

```
title: WhatsApp Messenger
developer: WhatsApp LLC
genre: Communication
score: 4.3
free: True
```

## Competitive Analysis

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

apps = {
    "WhatsApp": "com.whatsapp",
    "Telegram": "org.telegram.messenger",
    "Signal": "org.thoughtcrime.securesms",
}

results = []
for name, app_id in apps.items():
    try:
        data = scraper.app_get_fields(
            app_id,
            ["title", "score", "ratings", "installs", "icon"],
            lang="en",
            country="us",
            assets="SMALL",
        )
        data["name"] = name
        results.append(data)
    except Exception as exc:
        print(f"Error analysing {name}: {exc}")

results.sort(key=lambda item: item.get("score", 0), reverse=True)

print("Ranking by rating:")
for index, app in enumerate(results, start=1):
    print(f"{index}. {app['name']}: {app.get('score', 'N/A')} stars")
```

## Search and Filter Apps

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

results = scraper.search_analyze("fitness tracker", count=50, lang="en", country="us")
top_free = [app for app in results if app.get("free") and app.get("score", 0) >= 4.5]

print("Top free fitness apps:")
for app in top_free[:10]:
    print(f"{app['title']}: {app['score']} stars - {app['installs']}")
```

## Developer Portfolio

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
dev_id = "5700313618786177705"  # WhatsApp Inc.

apps = scraper.developer_analyze(dev_id, count=50, lang="en", country="us")

print(f"Developer has {len(apps)} apps:")
for app in apps:
    print(f"  {app['title']}: {app['score']} stars - {app['installs']}")
```

## Reviews with Sentiment Buckets

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
app_id = "com.whatsapp"

reviews = scraper.reviews_analyze(app_id, count=100, sort="NEWEST", lang="en", country="us")

ratings = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
for review in reviews:
    ratings[review["score"]] += 1

print("Ratings distribution:")
for stars, count in ratings.items():
    print(f"  {stars} stars: {count} reviews")

positive = [review for review in reviews if review["score"] >= 4]
print(f"\nPositive reviews: {len(positive)}/{len(reviews)}")
```

## Top Charts by Category

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

top_games = scraper.list_analyze("TOP_FREE", "GAME", count=50, lang="en", country="us")

print("Top 10 free games:")
for index, app in enumerate(top_games[:10], start=1):
    print(f"{index}. {app['title']} - {app['developer']}")
    print(f"   Rating: {app['score']} | Installs: {app['installs']}")

top_paid = scraper.list_analyze("TOP_PAID", "APPLICATION", count=20, lang="en", country="us")

print("\nTop 5 paid apps:")
for index, app in enumerate(top_paid[:5], start=1):
    print(f"{index}. {app['title']} - ${app['price']}")
```

## Find Similar Apps

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
app_id = "com.whatsapp"

similar = scraper.similar_analyze(app_id, count=30, lang="en", country="us")

print("Apps similar to WhatsApp:")
for app in similar[:10]:
    print(f"  {app['title']} by {app['developer']}")
    print(f"    Rating: {app['score']} | {app['installs']}")
```

## Search Suggestions

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

suggestions = scraper.suggest_analyze("photo editor", count=10, lang="en", country="us")
for suggestion in suggestions:
    print(f"  - {suggestion}")

nested = scraper.suggest_nested("fitness", count=5, lang="en", country="us")
for term, related in nested.items():
    print(f"{term}: {related}")
```

## Assets Parameter (Image Sizes)

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
app_id = "com.whatsapp"

small_icon = scraper.app_get_field(app_id, "icon", assets="SMALL")       # https://...=w512
medium_icon = scraper.app_get_field(app_id, "icon", assets="MEDIUM")     # https://...=w1024
large_icon = scraper.app_get_field(app_id, "icon", assets="LARGE")       # https://...=w2048
original_icon = scraper.app_get_field(app_id, "icon", assets="ORIGINAL") # https://...=w9999

media = scraper.app_get_fields(
    app_id,
    ["icon", "screenshots", "headerImage", "videoImage"],
    assets="ORIGINAL",
)

print(f"Icon: {media['icon']}")
print(f"Screenshots: {len(media['screenshots'])} images")
print(f"Header: {media['headerImage']}")

scraper.app_print_field(app_id, "icon", assets="LARGE")
scraper.app_print_all(app_id, assets="ORIGINAL")
```

## Multi-Language Support

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
app_id = "com.whatsapp"

languages = [
    ("en", "us", "English"),
    ("es", "es", "Spanish"),
    ("fr", "fr", "French"),
    ("de", "de", "German"),
]

for lang, country, label in languages:
    data = scraper.app_get_fields(app_id, ["title", "description"], lang=lang, country=country)
    print(f"\n{label}:")
    print(f"  Title: {data['title']}")
    print(f"  Description: {data['description'][:100]}...")
```

## HTTP Client Reminder

`GPlayScraper()` always uses `curl_cffi`; the HTTP backend is fixed and cannot be overridden.

## Real-World Use Cases

- **Market research** – Compare competitors to understand market positioning and user sentiment.
- **Keyword research** – Use search suggestions to discover popular keywords for ASO.
- **App monitoring** – Track scores, installs, and review trends over time.
- **Data analysis** – Feed structured data into dashboards, reports, or machine-learning pipelines.
- **Competitive intelligence** – Watch competitor updates, release cadence, and new features.
- **Image quality control** – Tune the `assets` parameter for the right image sizes:
  - `SMALL` (512px) – Thumbnails and mobile displays.
  - `MEDIUM` (1024px) – Default quality.
  - `LARGE` (2048px) – High-resolution presentation.
  - `ORIGINAL` – Maximum quality (use sparingly).
