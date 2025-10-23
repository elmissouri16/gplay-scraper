# Similar Methods

Find similar and related apps on Google Play Store based on a reference app.

## Quick Start

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

# Get similar apps
similar = scraper.similar_analyze("com.whatsapp", count=20)
for app in similar:
    print(f"{app['title']}: {app['score']}★ by {app['developer']}")

# Get specific fields
titles = scraper.similar_get_field("com.whatsapp", "title")
print(titles)

# Get multiple fields
apps = scraper.similar_get_fields("com.whatsapp", ["title", "score", "free"])
print(apps)
```

---

## HTTP Client

GPlay Scraper now relies exclusively on [`curl_cffi`](https://github.com/yifeikong/curl_cffi) with a Chrome fingerprint. Initialising `GPlayScraper()` without arguments uses this client automatically; overriding the HTTP backend is not supported.

---

## Methods

### `similar_analyze(app_id, count=100, lang='en', country='us')`
Returns similar apps as a list of dictionaries.

```python
similar = scraper.similar_analyze("com.whatsapp", count=20)
# Returns: [{'appId': '...', 'title': '...', 'score': 4.5, ...}, ...]
```

### `similar_get_field(app_id, field, count=100, lang='en', country='us')`
Returns a specific field from all similar apps.

```python
titles = scraper.similar_get_field("com.whatsapp", "title")
# Returns: ['App 1', 'App 2', 'App 3', ...]
```

### `similar_get_fields(app_id, fields, count=100, lang='en', country='us')`
Returns multiple fields from all similar apps.

```python
apps = scraper.similar_get_fields("com.whatsapp", ["title", "score", "free"])
# Returns: [{'title': 'App 1', 'score': 4.5, 'free': True}, ...]
```

### Formatting Tips

Use standard Python loops to present similar app data:

```python
apps = scraper.similar_get_fields("com.whatsapp", ["title", "score", "developer"], count=10)
for idx, app in enumerate(apps, 1):
    print(f"{idx}. {app['title']} — {app['score']}★ by {app['developer']}")
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

### Competitive Analysis
```python
app_id = "com.whatsapp"
similar = scraper.similar_get_fields(app_id, ["title", "score", "developer"], count=30)

print(f"Competitors of {app_id}:")
for i, app in enumerate(similar[:10], 1):
    print(f"{i}. {app['title']}: {app['score']}★ by {app['developer']}")

# Calculate average competitor rating
avg_score = sum(app['score'] or 0 for app in similar) / len(similar)
print(f"\nAverage competitor rating: {avg_score:.2f}★")
```

### Find Better Alternatives
```python
app_id = "com.example.app"
my_app = scraper.app_get_field(app_id, "score")
similar = scraper.similar_get_fields(app_id, ["title", "score", "url"], count=50)

# Find apps with higher ratings
better_apps = [app for app in similar if app['score'] and app['score'] > my_app]
better_apps.sort(key=lambda x: x['score'], reverse=True)

print(f"Apps better than {app_id} ({my_app}★):")
for app in better_apps[:10]:
    print(f"- {app['title']}: {app['score']}★")
```

### Market Positioning
```python
app_id = "com.whatsapp"
similar = scraper.similar_get_fields(app_id, ["title", "free", "price", "score"], count=50)

free_apps = [app for app in similar if app['free']]
paid_apps = [app for app in similar if not app['free']]

print(f"Market Analysis for {app_id}:")
print(f"  Free competitors: {len(free_apps)}")
print(f"  Paid competitors: {len(paid_apps)}")
if free_apps:
    print(f"  Free avg rating: {sum(a['score'] or 0 for a in free_apps)/len(free_apps):.2f}★")
if paid_apps:
    print(f"  Paid avg rating: {sum(a['score'] or 0 for a in paid_apps)/len(paid_apps):.2f}★")
```

### Developer Overlap Analysis
```python
from collections import Counter

app_id = "com.whatsapp"
similar = scraper.similar_get_field(app_id, "developer", count=50)

# Count apps per developer
developer_counts = Counter(similar)
top_developers = developer_counts.most_common(5)

print(f"Top developers in similar apps to {app_id}:")
for developer, count in top_developers:
    print(f"{developer}: {count} apps")
```

### Export Similar Apps
```python
import json

app_id = "com.whatsapp"
similar = scraper.similar_analyze(app_id, count=50)

with open(f'similar_to_{app_id}.json', 'w') as f:
    json.dump(similar, f, indent=2)

print(f"Exported {len(similar)} similar apps to similar_to_{app_id}.json")
```

### Compare Multiple Apps
```python
apps_to_compare = ["com.whatsapp", "com.telegram", "com.viber"]
all_similar = {}

for app_id in apps_to_compare:
    similar = scraper.similar_get_fields(app_id, ["appId", "title"], count=20)
    all_similar[app_id] = [app['appId'] for app in similar]
    print(f"{app_id}: {len(similar)} similar apps")

# Find common competitors
common = set(all_similar[apps_to_compare[0]])
for app_id in apps_to_compare[1:]:
    common &= set(all_similar[app_id])

print(f"\nCommon competitors: {len(common)}")
for app_id in list(common)[:5]:
    title = scraper.app_get_field(app_id, "title")
    print(f"- {title}")
```

### Feature Gap Analysis
```python
app_id = "com.whatsapp"
similar = scraper.similar_get_fields(app_id, ["title", "score"], count=30)

# Get top-rated competitors
top_competitors = sorted(similar, key=lambda x: x['score'] or 0, reverse=True)[:5]

print(f"Top-rated competitors of {app_id}:")
for i, app in enumerate(top_competitors, 1):
    print(f"{i}. {app['title']}: {app['score']}★")
    # You can then analyze these apps individually for features
```

### Price Comparison
```python
app_id = "com.example.paidapp"
my_price = scraper.app_get_field(app_id, "price")
similar = scraper.similar_get_fields(app_id, ["title", "price", "free"], count=50)

paid_similar = [app for app in similar if not app['free'] and app['price']]

if paid_similar:
    prices = [app['price'] for app in paid_similar]
    print(f"Price Comparison:")
    print(f"  Your app: ${my_price:.2f}")
    print(f"  Competitor min: ${min(prices):.2f}")
    print(f"  Competitor max: ${max(prices):.2f}")
    print(f"  Competitor avg: ${sum(prices)/len(prices):.2f}")
```

---

## Parameters

### Initialization

### Method Parameters
- `app_id` (str, required) - App package name to find similar apps for
- `count` (int, optional) - Maximum number of similar apps to return (default: 100)
- `lang` (str, optional) - Language code (default: 'en')
- `country` (str, optional) - Country code (default: 'us')
- `field` (str) - Single field name
- `fields` (List[str]) - List of field names

### Language & Country Codes
- **Language**: 'en', 'es', 'fr', 'de', 'ja', 'ko', 'pt', 'ru', 'zh', etc.
- **Country**: 'us', 'gb', 'ca', 'au', 'in', 'br', 'jp', 'kr', 'de', 'fr', etc.

---

## When to Use Each Method

- **`similar_analyze()`** - Need complete data for all similar apps
- **`similar_get_field()`** - Need just one field from all similar apps
- **`similar_get_fields()`** - Need specific fields from all similar apps (more efficient)
- **Standard Python formatting** - Use the returned data for custom reporting or display

---

## Use Cases

### Competitive Intelligence
- Identify direct competitors
- Monitor competitor ratings and pricing
- Track market positioning
- Discover new entrants in your category

### Market Research
- Understand market landscape
- Analyze pricing strategies
- Identify market gaps
- Study successful competitors

### Product Development
- Find feature inspiration
- Identify differentiation opportunities
- Benchmark against competitors
- Discover user expectations

### Marketing Strategy
- Identify target audience overlap
- Study competitor positioning
- Find partnership opportunities
- Analyze market trends

---

## Advanced Features

### Rate Limiting
Built-in rate limiting (1 second delay between requests) prevents blocking.

### Error Handling
```python
from gplay_scraper import GPlayScraper, AppNotFoundError, NetworkError

scraper = GPlayScraper()

try:
    similar = scraper.similar_analyze("invalid.app.id")
except AppNotFoundError:
    print("App not found or no similar apps available")
except NetworkError:
    print("Network error occurred")
```

### Multi-Region Similar Apps
```python
# Get similar apps from different regions
us_similar = scraper.similar_analyze("com.whatsapp", country="us", count=20)
uk_similar = scraper.similar_analyze("com.whatsapp", country="gb", count=20)
jp_similar = scraper.similar_analyze("com.whatsapp", country="jp", lang="ja", count=20)

print(f"US similar apps: {len(us_similar)}")
print(f"UK similar apps: {len(uk_similar)}")
print(f"JP similar apps: {len(jp_similar)}")
```

### Filtering Results
```python
similar = scraper.similar_analyze("com.whatsapp", count=50)

# Filter by rating
high_rated = [app for app in similar if app['score'] and app['score'] >= 4.0]

# Filter by price
free_apps = [app for app in similar if app['free']]

# Filter by developer
exclude_dev = [app for app in similar if app['developer'] != "WhatsApp LLC"]

print(f"High rated: {len(high_rated)}")
print(f"Free: {len(free_apps)}")
print(f"Other developers: {len(exclude_dev)}")
```

### Batch Analysis
```python
# Analyze similar apps for multiple apps
apps = ["com.whatsapp", "com.telegram", "com.viber"]
results = {}

for app_id in apps:
    similar = scraper.similar_get_fields(app_id, ["title", "score"], count=10)
    results[app_id] = similar
    print(f"{app_id}: {len(similar)} similar apps found")
```
