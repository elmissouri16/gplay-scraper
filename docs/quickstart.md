# Quick Start Guide

This guide walks through the core workflows supported by GPlay Scraper.

## Basic Usage

### Import and Initialise

```python
from gplay_scraper import GPlayScraper

# Networking is handled internally
scraper = GPlayScraper()
```

## 7 Method Types

GPlay Scraper exposes seven method families. Most families offer the same five helpers:

- `analyze()` – Fetch all data as a dictionary or list.
- `get_field()` – Fetch a single field.
- `get_fields()` – Fetch a subset of fields efficiently.

Suggest methods additionally provide `nested()` for exploring suggestions-of-suggestions.

### Method Families

1. **App Methods** – Extract 65+ fields from any app.
2. **Search Methods** – Search for apps by keyword.
3. **Reviews Methods** – Retrieve user reviews and metadata.
4. **Developer Methods** – Fetch all apps published by a developer.
5. **List Methods** – Access Play Store charts (free, paid, grossing).
6. **Similar Methods** – Discover related/competitor apps.
7. **Suggest Methods** – Get search suggestions and autocomplete terms.

## Common Parameters

All method families share the following arguments:

- `lang` – ISO language code (default `"en"`).
- `country` – ISO country code (default `"us"`).
- `count` – Number of results to return when pagination applies.

```python
scraper.app_analyze("com.whatsapp", lang="es", country="es")
scraper.app_analyze("com.whatsapp", lang="fr", country="fr")
results = scraper.search_get_fields("productivity", ["title", "developer"], count=25, lang="en", country="us")
print(results[:3])
```

## Method Recipes

### 1. App Methods

```python
app_id = "com.whatsapp"

data = scraper.app_analyze(app_id, lang="en", country="us")
print(f"Title: {data['title']}")
print(f"Rating: {data['score']}")

title = scraper.app_get_field(app_id, "title", lang="en", country="us")

fields = scraper.app_get_fields(app_id, ["title", "score", "installs"])
print(f"{fields['title']} — {fields['score']}★ — {fields['installs']} installs")
```

### 2. Search Methods

```python
query = "social media"

results = scraper.search_analyze(query, count=20, lang="en", country="us")
for app in results:
    print(f"{app['title']} - {app['developer']}")

titles = scraper.search_get_field(query, "title", count=10)
data = scraper.search_get_fields(query, ["title", "score"], count=10)
for idx, app in enumerate(data[:5], 1):
    print(f"{idx}. {app['title']} — {app.get('score', 'N/A')}★")
```

### 3. Reviews Methods

```python
app_id = "com.whatsapp"

reviews = scraper.reviews_analyze(app_id, count=50, sort="NEWEST")
for review in reviews:
    print(f"{review['userName']}: {review['score']} stars")

scores = scraper.reviews_get_field(app_id, "score", count=100, sort="NEWEST")
recent = scraper.reviews_get_fields(app_id, ["userName", "score"], count=50, sort="NEWEST")
print(f"First reviewer: {recent[0]['userName']} ({recent[0]['score']}★)")
```

### 4. Developer Methods

```python
dev_id = "5700313618786177705"  # WhatsApp Inc.

apps = scraper.developer_analyze(dev_id, count=20, lang="en", country="us")
for app in apps:
    print(f"{app['title']} - {app['score']} stars")

titles = scraper.developer_get_field(dev_id, "title", count=20)
summaries = scraper.developer_get_fields(dev_id, ["title", "score"], count=20)
print(summaries[:3])
```

### 5. List Methods

```python
# Collections: TOP_FREE, TOP_PAID, TOP_GROSSING
# Categories: GAME, SOCIAL, COMMUNICATION, etc.

apps = scraper.list_analyze("TOP_FREE", "GAME", count=50)
for app in apps:
    print(f"{app['title']} - {app['installs']}")
```

### 6. Similar Methods

```python
app_id = "com.whatsapp"

similar = scraper.similar_analyze(app_id, count=30, lang="en", country="us")
for app in similar:
    print(f"{app['title']} - {app['developer']}")
```

### 7. Suggest Methods

```python
suggestions = scraper.suggest_analyze("fitness", count=5, lang="en", country="us")
print(suggestions)
```
