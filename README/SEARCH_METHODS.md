# Search Methods

Search for apps on Google Play Store by keyword, app name, or category.

## Quick Start

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

# Search for apps
results = scraper.search_analyze("social media", count=20)
for app in results:
    print(f"{app['title']}: {app['score']}★ by {app['developer']}")

# Get specific fields
titles = scraper.search_get_field("fitness tracker", "title")
print(titles)

# Get multiple fields
apps = scraper.search_get_fields("photo editor", ["title", "score", "free"])
print(apps)
```

---

## HTTP Client

GPlay Scraper now relies exclusively on [`curl_cffi`](https://github.com/yifeikong/curl_cffi) with a Chrome fingerprint. Initialising `GPlayScraper()` without arguments uses this client automatically; overriding the HTTP backend is not supported.

---

## Methods

### `search_analyze(query, count=100, lang='en', country='us')`
Returns search results as a list of dictionaries.

```python
results = scraper.search_analyze("social media", count=20)
# Returns: [{'appId': '...', 'title': '...', 'score': 4.5, ...}, ...]
```

### `search_get_field(query, field, count=100, lang='en', country='us')`
Returns a specific field from all search results.

```python
titles = scraper.search_get_field("fitness tracker", "title")
# Returns: ['App 1', 'App 2', 'App 3', ...]
```

### `search_get_fields(query, fields, count=100, lang='en', country='us')`
Returns multiple fields from all search results.

```python
apps = scraper.search_get_fields("photo editor", ["title", "score", "free"])
# Returns: [{'title': 'App 1', 'score': 4.5, 'free': True}, ...]
```

### `search_print_field(query, field, count=100, lang='en', country='us')`
Prints a specific field from all search results.

```python
scraper.search_print_field("social media", "title", count=10)
# Output:
# 0. title: App 1
# 1. title: App 2
# 2. title: App 3
```

### `search_print_fields(query, fields, count=100, lang='en', country='us')`
Prints multiple fields from all search results.

```python
scraper.search_print_fields("social media", ["title", "score"], count=10)
# Output:
# 0. title: App 1, score: 4.5
# 1. title: App 2, score: 4.2
```

## Available Fields

- `appId` - App package name (e.g., "com.example.app")
- `title` - App name
- `description` - App description/summary
- `icon` - App icon URL
- `url` - Play Store URL
- `developer` - Developer name
- `score` - Average rating (1-5)
- `scoreText` - Rating as text (e.g., "4.5")
- `currency` - Price currency (e.g., "USD")
- `price` - App price (0 if free)
- `free` - Boolean, true if free

---

## Practical Examples

### Find Top-Rated Apps
```python
results = scraper.search_get_fields("productivity", ["title", "score", "developer"], count=50)

# Filter high-rated apps
top_rated = [app for app in results if app['score'] and app['score'] >= 4.5]
top_rated.sort(key=lambda x: x['score'], reverse=True)

print("Top-Rated Productivity Apps:")
for i, app in enumerate(top_rated[:10], 1):
    print(f"{i}. {app['title']}: {app['score']}★ by {app['developer']}")
```

### Compare Free vs Paid Apps
```python
results = scraper.search_get_fields("photo editor", ["title", "free", "price", "score"], count=50)

free_apps = [app for app in results if app['free']]
paid_apps = [app for app in results if not app['free']]

free_avg = sum(app['score'] or 0 for app in free_apps) / len(free_apps) if free_apps else 0
paid_avg = sum(app['score'] or 0 for app in paid_apps) / len(paid_apps) if paid_apps else 0

print(f"Free apps: {len(free_apps)} (avg: {free_avg:.2f}★)")
print(f"Paid apps: {len(paid_apps)} (avg: {paid_avg:.2f}★)")
```

### Market Research
```python
keywords = ["fitness", "meditation", "diet", "sleep tracker"]

for keyword in keywords:
    results = scraper.search_get_fields(keyword, ["title", "score"], count=10)
    avg_score = sum(app['score'] or 0 for app in results) / len(results)
    print(f"{keyword}: {len(results)} apps, avg {avg_score:.2f}★")
```

### Find Competitors
```python
query = "task manager"
results = scraper.search_get_fields(query, ["title", "developer", "score", "free"], count=30)

print(f"Competitors for '{query}':")
for i, app in enumerate(results[:15], 1):
    price = "Free" if app['free'] else f"${app.get('price', 'N/A')}"
    print(f"{i}. {app['title']} by {app['developer']} - {app['score']}★ ({price})")
```

### Export Search Results
```python
import json

query = "language learning"
results = scraper.search_analyze(query, count=100)

with open(f'search_{query.replace(" ", "_")}.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"Exported {len(results)} results for '{query}'")
```

### Multi-Keyword Search
```python
keywords = ["vpn", "proxy", "security"]
all_results = {}

for keyword in keywords:
    results = scraper.search_get_fields(keyword, ["appId", "title", "score"], count=20)
    all_results[keyword] = results
    print(f"{keyword}: {len(results)} apps found")

# Find apps appearing in multiple searches
app_ids = {}
for keyword, results in all_results.items():
    for app in results:
        app_id = app['appId']
        if app_id not in app_ids:
            app_ids[app_id] = {'title': app['title'], 'keywords': []}
        app_ids[app_id]['keywords'].append(keyword)

# Apps in multiple categories
multi_category = {aid: data for aid, data in app_ids.items() if len(data['keywords']) > 1}
print(f"\nApps in multiple categories: {len(multi_category)}")
for app_id, data in list(multi_category.items())[:5]:
    print(f"- {data['title']}: {', '.join(data['keywords'])}")
```

### Analyze Developer Presence
```python
from collections import Counter

query = "puzzle game"
results = scraper.search_get_field(query, "developer", count=100)

# Count apps per developer
developer_counts = Counter(results)
top_developers = developer_counts.most_common(10)

print(f"Top Developers in '{query}':")
for developer, count in top_developers:
    print(f"{developer}: {count} apps")
```

### Price Range Analysis
```python
query = "premium photo editor"
results = scraper.search_get_fields(query, ["title", "price", "free"], count=50)

paid_apps = [app for app in results if not app['free'] and app['price']]

if paid_apps:
    prices = [app['price'] for app in paid_apps]
    print(f"Price Analysis for '{query}':")
    print(f"  Min: ${min(prices):.2f}")
    print(f"  Max: ${max(prices):.2f}")
    print(f"  Avg: ${sum(prices)/len(prices):.2f}")
    print(f"  Total paid apps: {len(paid_apps)}")
```

---

## Parameters

### Initialization

### Method Parameters
- `query` (str, required) - Search keyword or phrase
- `count` (int, optional) - Maximum number of results to return (default: 100)
- `lang` (str, optional) - Language code (default: 'en')
- `country` (str, optional) - Country code (default: 'us')
- `field` (str) - Single field name
- `fields` (List[str]) - List of field names

### Search Query Tips
- Use specific keywords: "fitness tracker" vs "fitness"
- Try app categories: "puzzle game", "photo editor"
- Search by functionality: "vpn", "password manager"
- Use brand names: "google", "microsoft"
- Combine terms: "free music player"

### Language & Country Codes
- **Language**: 'en', 'es', 'fr', 'de', 'ja', 'ko', 'pt', 'ru', 'zh', etc.
- **Country**: 'us', 'gb', 'ca', 'au', 'in', 'br', 'jp', 'kr', 'de', 'fr', etc.

---

## When to Use Each Method

- **`search_analyze()`** - Need complete data for all search results
- **`search_get_field()`** - Need just one field from all results
- **`search_get_fields()`** - Need specific fields from all results (more efficient)
- **`search_print_field()`** - Quick debugging/console output
- **`search_print_fields()`** - Quick debugging of multiple fields
- **`search_print_fields()`** - Explore available data structure

---

## Advanced Features

### Rate Limiting
Built-in rate limiting (1 second delay between requests) prevents blocking.

### Error Handling
```python
from gplay_scraper import GPlayScraper, AppNotFoundError, NetworkError

scraper = GPlayScraper()

try:
    results = scraper.search_analyze("")
except ValueError:
    print("Query cannot be empty")
except NetworkError:
    print("Network error occurred")
```

### Multi-Region Search
```python
# Search in different regions
us_results = scraper.search_analyze("vpn", country="us", count=20)
uk_results = scraper.search_analyze("vpn", country="gb", count=20)
jp_results = scraper.search_analyze("vpn", country="jp", lang="ja", count=20)

print(f"US: {len(us_results)} results")
print(f"UK: {len(uk_results)} results")
print(f"JP: {len(jp_results)} results")
```

### Pagination
```python
# Get more results
results_20 = scraper.search_analyze("game", count=20)
results_50 = scraper.search_analyze("game", count=50)
results_100 = scraper.search_analyze("game", count=100)

print(f"20 results: {len(results_20)}")
print(f"50 results: {len(results_50)}")
print(f"100 results: {len(results_100)}")
```

### Search Result Filtering
```python
results = scraper.search_analyze("music player", count=50)

# Filter by rating
high_rated = [app for app in results if app['score'] and app['score'] >= 4.0]

# Filter by price
free_apps = [app for app in results if app['free']]

# Filter by developer
google_apps = [app for app in results if 'google' in app['developer'].lower()]

print(f"High rated: {len(high_rated)}")
print(f"Free: {len(free_apps)}")
print(f"Google: {len(google_apps)}")
```
