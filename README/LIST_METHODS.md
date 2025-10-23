# List Methods

Get top charts from Google Play Store (top free, top paid, top grossing).

## Quick Start

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

# Get top free apps
top_free = scraper.list_analyze("TOP_FREE", "GAME", count=50)
for app in top_free[:10]:
    print(f"{app['title']}: {app['installs']} installs")

# Get specific fields
titles = scraper.list_get_field("TOP_FREE", "title", "APPLICATION")
print(titles)

# Get multiple fields
apps = scraper.list_get_fields("TOP_PAID", ["title", "price", "score"], "GAME")
print(apps)
```

## Methods

### `list_analyze(collection='TOP_FREE', category='APPLICATION', count=100, lang='en', country='us')`
Returns top chart apps as a list of dictionaries.

```python
apps = scraper.list_analyze("TOP_FREE", "GAME", count=50)
# Returns: [{'appId': '...', 'title': '...', 'installs': '...', ...}, ...]
```

### `list_get_field(collection, field, category='APPLICATION', count=100, lang='en', country='us')`
Returns a specific field from all chart apps.

```python
titles = scraper.list_get_field("TOP_FREE", "title", "APPLICATION")
# Returns: ['App 1', 'App 2', 'App 3', ...]
```

### `list_get_fields(collection, fields, category='APPLICATION', count=100, lang='en', country='us')`
Returns multiple fields from all chart apps.

```python
apps = scraper.list_get_fields("TOP_PAID", ["title", "price", "score"], "GAME")
# Returns: [{'title': 'App 1', 'price': 4.99, 'score': 4.5}, ...]
```

### Formatting Tips

Use standard Python formatting to present chart data:

```python
apps = scraper.list_get_fields("TOP_FREE", ["title", "score"], "GAME", count=10)
for idx, app in enumerate(apps, 1):
    print(f"{idx}. {app['title']} — {app['score']}★")
```

## Available Fields

- `appId` - App package name (e.g., "com.example.app")
- `title` - App name
- `description` - App description
- `icon` - App icon URL
- `screenshots` - List of screenshot URLs
- `url` - Play Store URL
- `developer` - Developer name
- `genre` - App category
- `score` - Average rating (1-5)
- `scoreText` - Rating as text (e.g., "4.5")
- `installs` - Install count (e.g., "10,000,000+")
- `currency` - Price currency (e.g., "USD")
- `price` - App price (0 if free)
- `free` - Boolean, true if free

---

## Collection Types

### Available Collections
- **`TOP_FREE`** - Top free apps (most popular free apps)
- **`TOP_PAID`** - Top paid apps (most popular paid apps)
- **`TOP_GROSSING`** - Top grossing apps (highest revenue apps)

---

## Categories

### App Categories (36)
- `APPLICATION` - All apps (default)
- `ANDROID_WEAR` - Android Wear apps
- `ART_AND_DESIGN` - Art & design
- `AUTO_AND_VEHICLES` - Auto & vehicles
- `BEAUTY` - Beauty
- `BOOKS_AND_REFERENCE` - Books & reference
- `BUSINESS` - Business
- `COMICS` - Comics
- `COMMUNICATION` - Communication
- `DATING` - Dating
- `EDUCATION` - Education
- `ENTERTAINMENT` - Entertainment
- `EVENTS` - Events
- `FINANCE` - Finance
- `FOOD_AND_DRINK` - Food & drink
- `HEALTH_AND_FITNESS` - Health & fitness
- `HOUSE_AND_HOME` - House & home
- `LIBRARIES_AND_DEMO` - Libraries & demo
- `LIFESTYLE` - Lifestyle
- `MAPS_AND_NAVIGATION` - Maps & navigation
- `MEDICAL` - Medical
- `MUSIC_AND_AUDIO` - Music & audio
- `NEWS_AND_MAGAZINES` - News & magazines
- `PARENTING` - Parenting
- `PERSONALIZATION` - Personalization
- `PHOTOGRAPHY` - Photography
- `PRODUCTIVITY` - Productivity
- `SHOPPING` - Shopping
- `SOCIAL` - Social
- `SPORTS` - Sports
- `TOOLS` - Tools
- `TRAVEL_AND_LOCAL` - Travel & local
- `VIDEO_PLAYERS` - Video players & editors
- `WATCH_FACE` - Watch faces
- `WEATHER` - Weather
- `FAMILY` - Family

### Game Categories (18)
- `GAME` - All games
- `GAME_ACTION` - Action games
- `GAME_ADVENTURE` - Adventure games
- `GAME_ARCADE` - Arcade games
- `GAME_BOARD` - Board games
- `GAME_CARD` - Card games
- `GAME_CASINO` - Casino games
- `GAME_CASUAL` - Casual games
- `GAME_EDUCATIONAL` - Educational games
- `GAME_MUSIC` - Music games
- `GAME_PUZZLE` - Puzzle games
- `GAME_RACING` - Racing games
- `GAME_ROLE_PLAYING` - Role playing games
- `GAME_SIMULATION` - Simulation games
- `GAME_SPORTS` - Sports games
- `GAME_STRATEGY` - Strategy games
- `GAME_TRIVIA` - Trivia games
- `GAME_WORD` - Word games

---

## Practical Examples

### Top Free Games Analysis
```python
top_games = scraper.list_analyze("TOP_FREE", "GAME", count=100)

print(f"Total games: {len(top_games)}")
print(f"Average rating: {sum(a['score'] for a in top_games if a['score']) / len(top_games):.2f}")
print(f"\nTop 5 games:")
for i, game in enumerate(top_games[:5], 1):
    print(f"{i}. {game['title']} - {game['score']}★ - {game['installs']} installs")
```

### Compare Free vs Paid Apps
```python
top_free = scraper.list_get_fields("TOP_FREE", ["title", "score", "installs"], "APPLICATION", count=50)
top_paid = scraper.list_get_fields("TOP_PAID", ["title", "score", "price"], "APPLICATION", count=50)

free_avg = sum(a['score'] or 0 for a in top_free) / len(top_free)
paid_avg = sum(a['score'] or 0 for a in top_paid) / len(top_paid)

print(f"Top Free Apps - Avg Rating: {free_avg:.2f}")
print(f"Top Paid Apps - Avg Rating: {paid_avg:.2f}")
```

### Find Highest Grossing Apps
```python
top_grossing = scraper.list_get_fields("TOP_GROSSING", ["title", "developer", "genre"], "APPLICATION", count=20)

print("Top 10 Highest Grossing Apps:")
for i, app in enumerate(top_grossing[:10], 1):
    print(f"{i}. {app['title']} by {app['developer']} ({app['genre']})")
```

### Category Comparison
```python
categories = ["GAME", "SOCIAL", "PRODUCTIVITY", "ENTERTAINMENT"]

for category in categories:
    apps = scraper.list_get_fields("TOP_FREE", ["title", "score"], category, count=10)
    avg_score = sum(a['score'] or 0 for a in apps) / len(apps)
    print(f"{category}: {avg_score:.2f}★ average")
```

### Game Genre Analysis
```python
game_genres = ["GAME_ACTION", "GAME_PUZZLE", "GAME_CASUAL", "GAME_STRATEGY"]

for genre in game_genres:
    games = scraper.list_get_fields("TOP_FREE", ["title", "score", "installs"], genre, count=5)
    print(f"\n{genre}:")
    for i, game in enumerate(games, 1):
        print(f"  {i}. {game['title']} - {game['score']}★")
```

### Export Top Charts
```python
import json

top_free = scraper.list_analyze("TOP_FREE", "GAME", count=100)

with open('top_free_games.json', 'w') as f:
    json.dump(top_free, f, indent=2)

print(f"Exported {len(top_free)} games to top_free_games.json")
```

### Track Chart Positions
```python
import time
import json
from datetime import datetime

def track_charts():
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "top_free": scraper.list_get_fields("TOP_FREE", ["title", "score"], "GAME", count=10),
        "top_paid": scraper.list_get_fields("TOP_PAID", ["title", "price"], "GAME", count=10)
    }
    
    with open(f'charts_{datetime.now().strftime("%Y%m%d")}.json', 'w') as f:
        json.dump(snapshot, f, indent=2)
    
    print(f"Snapshot saved at {snapshot['timestamp']}")

track_charts()
```

---

## Parameters

### Initialization

### Method Parameters
- `collection` (str) - Chart type: "TOP_FREE", "TOP_PAID", "TOP_GROSSING" (default: "TOP_FREE")
- `category` (str, optional) - Category filter (default: "APPLICATION")
- `count` (int, optional) - Maximum number of apps to return (default: 100)
- `lang` (str, optional) - Language code (default: 'en')
- `country` (str, optional) - Country code (default: 'us')
- `field` (str) - Single field name
- `fields` (List[str]) - List of field names

### Language & Country Codes
- **Language**: 'en', 'es', 'fr', 'de', 'ja', 'ko', 'pt', 'ru', 'zh', etc.
- **Country**: 'us', 'gb', 'ca', 'au', 'in', 'br', 'jp', 'kr', 'de', 'fr', etc.

---

## When to Use Each Method

- **`list_analyze()`** - Need complete data for all chart apps
- **`list_get_field()`** - Need just one field from all apps
- **`list_get_fields()`** - Need specific fields from all apps (more efficient)
- **Standard Python formatting** - Use the returned data for custom console output or reporting

---

## Advanced Features

### Rate Limiting
Built-in rate limiting (1 second delay between requests) prevents blocking.

### Error Handling
```python
from gplay_scraper import GPlayScraper, AppNotFoundError, NetworkError

scraper = GPlayScraper()

try:
    apps = scraper.list_analyze("INVALID_COLLECTION", "GAME")
except AppNotFoundError:
    print("Collection not found")
except NetworkError:
    print("Network error occurred")
```

### Multi-Region Charts
```python
# Get charts from different regions
us_charts = scraper.list_analyze("TOP_FREE", "GAME", country="us")
uk_charts = scraper.list_analyze("TOP_FREE", "GAME", country="gb")
jp_charts = scraper.list_analyze("TOP_FREE", "GAME", country="jp", lang="ja")

print(f"US Top Game: {us_charts[0]['title']}")
print(f"UK Top Game: {uk_charts[0]['title']}")
print(f"JP Top Game: {jp_charts[0]['title']}")
```

### Batch Analysis
```python
# Analyze multiple collections at once
collections = ["TOP_FREE", "TOP_PAID", "TOP_GROSSING"]
results = {}

for collection in collections:
    apps = scraper.list_get_fields(collection, ["title", "score"], "GAME", count=10)
    results[collection] = apps
    print(f"{collection}: {len(apps)} apps retrieved")
```
