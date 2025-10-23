# Developer Methods

Get all apps published by a specific developer on Google Play Store.

## Quick Start

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

# Get all apps from a developer
apps = scraper.developer_analyze("5700313618786177705")
for app in apps:
    print(f"{app['title']}: {app['score']}★")

# Get specific fields
titles = scraper.developer_get_field("5700313618786177705", "title")
print(titles)

# Get multiple fields
apps = scraper.developer_get_fields("5700313618786177705", ["title", "score", "free"])
print(apps)
```

---

## HTTP Client

GPlay Scraper now relies exclusively on [`curl_cffi`](https://github.com/yifeikong/curl_cffi) with a Chrome fingerprint. Initialising `GPlayScraper()` without arguments uses this client automatically; overriding the HTTP backend is not supported.

---

## Methods

### `developer_analyze(dev_id, count=100, lang='en', country='us')`
Returns all apps from a developer as a list of dictionaries.

```python
apps = scraper.developer_analyze("5700313618786177705", count=50)
# Returns: [{'appId': '...', 'title': '...', 'score': 4.5, ...}, ...]
```

### `developer_get_field(dev_id, field, count=100, lang='en', country='us')`
Returns a specific field from all developer apps.

```python
titles = scraper.developer_get_field("5700313618786177705", "title")
# Returns: ['App 1', 'App 2', 'App 3', ...]
```

### `developer_get_fields(dev_id, fields, count=100, lang='en', country='us')`
Returns multiple fields from all developer apps.

```python
apps = scraper.developer_get_fields("5700313618786177705", ["title", "score", "free"])
# Returns: [{'title': 'App 1', 'score': 4.5, 'free': True}, ...]
```

### Formatting Tips

Use standard Python formatting to display the data returned by `developer_get_field()` or `developer_get_fields()`:

```python
apps = scraper.developer_get_fields("5700313618786177705", ["title", "score"])
for idx, app in enumerate(apps[:5], 1):
    print(f"{idx}. {app['title']} — {app['score']}★")
```

## Available Fields

- `appId` - App package name (e.g., "com.example.app")
- `title` - App name
- `description` - App description
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

### Analyze Developer Portfolio
```python
dev_id = "5700313618786177705"
apps = scraper.developer_analyze(dev_id)

print(f"Total apps: {len(apps)}")
print(f"Average rating: {sum(a['score'] for a in apps if a['score']) / len(apps):.2f}")
print(f"Free apps: {sum(1 for a in apps if a['free'])}")
print(f"Paid apps: {sum(1 for a in apps if not a['free'])}")
```

### Find Top-Rated Apps
```python
dev_id = "5700313618786177705"
apps = scraper.developer_get_fields(dev_id, ["title", "score"])

# Sort by rating
top_apps = sorted(apps, key=lambda x: x['score'] or 0, reverse=True)[:5]
for i, app in enumerate(top_apps, 1):
    print(f"{i}. {app['title']}: {app['score']}★")
```

### Compare Free vs Paid Apps
```python
dev_id = "5700313618786177705"
apps = scraper.developer_get_fields(dev_id, ["title", "free", "price", "score"])

free_apps = [a for a in apps if a['free']]
paid_apps = [a for a in apps if not a['free']]

print(f"Free apps: {len(free_apps)} (avg rating: {sum(a['score'] or 0 for a in free_apps)/len(free_apps):.2f})")
print(f"Paid apps: {len(paid_apps)} (avg rating: {sum(a['score'] or 0 for a in paid_apps)/len(paid_apps):.2f})")
```

### Export Developer Apps
```python
import json

dev_id = "5700313618786177705"
apps = scraper.developer_analyze(dev_id)

with open('developer_apps.json', 'w') as f:
    json.dump(apps, f, indent=2)

print(f"Exported {len(apps)} apps to developer_apps.json")
```

---

## Parameters

### Initialization

### Method Parameters
- `dev_id` (str, required) - Developer ID (numeric or string)
- `count` (int, optional) - Maximum number of apps to return (default: 100)
- `lang` (str, optional) - Language code (default: 'en')
- `country` (str, optional) - Country code (default: 'us')
- `field` (str) - Single field name
- `fields` (List[str]) - List of field names

### Finding Developer IDs

**Method 1: From Developer Page URL**
- Numeric ID: `https://play.google.com/store/apps/dev?id=5700313618786177705`
  - Developer ID: `5700313618786177705`

- String ID: `https://play.google.com/store/apps/developer?id=Google+LLC`
  - Developer ID: `Google+LLC` or `Google LLC`

**Method 2: From App Page**
1. Go to any app by the developer
2. Click on the developer name
3. Extract ID from the URL

### Language & Country Codes
- **Language**: 'en', 'es', 'fr', 'de', 'ja', 'ko', 'pt', 'ru', 'zh', etc.
- **Country**: 'us', 'gb', 'ca', 'au', 'in', 'br', 'jp', 'kr', 'de', 'fr', etc.

---

## When to Use Each Method

- **`developer_analyze()`** - Need complete data for all apps
- **`developer_get_field()`** - Need just one field from all apps
- **`developer_get_fields()`** - Need specific fields from all apps (more efficient)
- **Standard Python formatting** - Use the returned lists/dictionaries for custom console output or storage

---

## Advanced Features

### Rate Limiting
Built-in rate limiting (1 second delay between requests) prevents blocking.

### Error Handling
```python
from gplay_scraper import GPlayScraper, AppNotFoundError, NetworkError

scraper = GPlayScraper()

try:
    apps = scraper.developer_analyze("invalid_dev_id")
except AppNotFoundError:
    print("Developer not found")
except NetworkError:
    print("Network error occurred")
```

### Multi-Region Data
```python
# Get developer apps from different regions
us_apps = scraper.developer_analyze("5700313618786177705", country="us")
uk_apps = scraper.developer_analyze("5700313618786177705", country="gb")
jp_apps = scraper.developer_analyze("5700313618786177705", country="jp", lang="ja")
```

### Pagination
```python
# Get first 50 apps
apps_batch1 = scraper.developer_analyze("5700313618786177705", count=50)

# Get more apps (library handles this automatically up to count limit)
apps_all = scraper.developer_analyze("5700313618786177705", count=200)
```
