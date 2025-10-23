# Google Play Scraper - Python Library 📱

[![PyPI version](https://badge.fury.io/py/gplay-scraper.svg)](https://badge.fury.io/py/gplay-scraper)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/gplay-scraper)](https://pepy.tech/project/gplay-scraper)
[![GitHub stars](https://img.shields.io/github/stars/Mohammedcha/gplay-scraper.svg)](https://github.com/Mohammedcha/gplay-scraper/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/Mohammedcha/gplay-scraper.svg)](https://github.com/Mohammedcha/gplay-scraper/issues)

<div align="center">
  <img src="https://github.com/Mohammedcha/gplay-scraper/blob/main/assets/gplay-scraper.png" alt="GPlay Scraper">
</div>

**GPlay Scraper** is a powerful Python library for extracting comprehensive data from the Google Play Store. Built for developers, data analysts, and researchers, it provides easy access to app information, user reviews, search results, top charts, and market intelligence—all without requiring API keys.

## 🎯 What Can You Scrape?

**App Data (65+ Fields)**
- Basic info: title, developer, description, category, genre
- Ratings & reviews: score, ratings count, histogram, user reviews
- Install metrics: install count ranges, download statistics
- Pricing: free/paid status, price, in-app purchases, currency
- Media: icon, screenshots, video, header image URLs
- Technical: version, size, Android version, release date, last update
- Content: age rating, privacy policy, developer contact info
- Features: permissions, what's new, developer website

**Search & Discovery**
- Search apps by keyword with filtering and pagination
- Get search suggestions and autocomplete terms
- Find similar/competitor apps for any app
- Access top charts (free, paid, grossing) across 54 categories

**Developer Intelligence**
- Get complete app portfolio for any developer
- Track developer's app performance and ratings
- Analyze developer's market presence

**User Reviews**
- Extract reviews with ratings, text, and timestamps
- Get reviewer names and helpful vote counts
- Filter by newest, most relevant, or highest rated
- Track app versions mentioned in reviews

**Market Research**
- Multi-language support (100+ languages)
- Multi-region data (150+ countries)
- Localized pricing and availability
- Competitive analysis and benchmarking

## 🆕 **What's New in v1.0.4** 

**✅ Assets Parameter:**
- **Configurable Image Sizes** - Control image quality for icons, screenshots, and media
- **4 Size Options** - SMALL (512px), MEDIUM (1024px), LARGE (2048px), ORIGINAL (max)
- **All App Methods** - Available in app_analyze(), app_get_field(), app_get_fields()
- **Release Date Fallback** - Fixed missing release dates with automatic fallback requests
- **Path Resolution** - Improved data extraction reliability

**✅ 7 Method Types:**
- **App Methods** - Extract 65+ data fields from any app (ratings, installs, pricing, permissions, etc.)
- **Search Methods** - Search Google Play Store apps with comprehensive filtering
- **Reviews Methods** - Extract user reviews with ratings, timestamps, and detailed feedback
- **Developer Methods** - Get all apps published by a specific developer
- **List Methods** - Access top charts (top free, top paid, top grossing) by category
- **Similar Methods** - Find similar/competitor apps for market research
- **Suggest Methods** - Get search suggestions and autocomplete for ASO

## ⚡ Key Features

**Powerful & Flexible**
- **20 functions across 7 method types** - analyze(), get_field(), get_fields()
- **No API keys required** - Direct scraping from Google Play Store
- **Multi-language & multi-region** - 100+ languages, 150+ countries

**Reliable & Safe**
- **Built-in rate limiting** - Prevents blocking with automatic delays
- **Resilient session management** - Single shared session with retry handling
- **Error handling** - Graceful failures with informative messages
- **Retry logic** - Automatic retries for failed requests

**Developer Friendly**
- **Simple API** - Intuitive method names and parameters
- **Comprehensive documentation** - Examples for every use case
- **Type hints** - Full IDE autocomplete support
- **Flexible output** - Get data as dict/list or print as JSON

## 📋 Requirements

- Python 3.7+

## 🚀 Installation

```bash
# Install from PyPI (standard workflow)
pip install gplay-scraper

# Alternatively install with uv
uv pip install gplay-scraper

# Develop locally in editable mode
pip install -e .
# or
uv pip install --editable .
```

## 📖 Quick Start

```python
from gplay_scraper import GPlayScraper

# Initialize scraper
scraper = GPlayScraper()

# Route traffic through a proxy (string applies to both http/https)
scraper_with_proxy = GPlayScraper(proxies="http://127.0.0.1:8080")

# Or provide a mapping for different schemes
scraper_with_split_proxy = GPlayScraper(
    proxies={
        "http": "http://corp-proxy.local:8080",
        "https": "http://secure-proxy.local:8443",
    }
)

# Update proxy configuration at runtime
scraper_with_proxy.set_proxies(None)  # Disable proxy when no longer needed

# Get app details with different image sizes
app_id = "com.whatsapp"
app_summary = scraper.app_get_fields(app_id, ["title", "score"], lang="en", country="us", assets="LARGE")
print(f"{app_summary['title']} — {app_summary['score']}★")

# Get high-quality app data
data = scraper.app_analyze(app_id, assets="ORIGINAL")  # Maximum image quality
icon_small = scraper.app_get_field(app_id, "icon", assets="SMALL")  # 512px icon

# Print specific fields with custom image sizes
large_icon = scraper.app_get_field(app_id, "icon", assets="LARGE")
media = scraper.app_get_fields(app_id, ["icon", "screenshots"], assets="ORIGINAL")
print(f"Large icon url: {large_icon}")
print(f"Screenshots available: {len(media['screenshots'])}")

# Search for apps
search_results = scraper.search_get_fields("social media", ["title", "developer"], count=10, lang="en", country="us")
for result in search_results[:3]:
    print(f"{result['title']} by {result['developer']}")

# Get reviews
recent_reviews = scraper.reviews_get_fields(app_id, ["userName", "score"], count=50, sort="NEWEST", lang="en", country="us")
print(f"Most recent reviewer: {recent_reviews[0]['userName']} ({recent_reviews[0]['score']}★)")

# Get developer apps
developer_apps = scraper.developer_get_fields("5700313618786177705", ["title", "score"], count=20, lang="en", country="us")
print(f"Developer portfolio size: {len(developer_apps)}")

# Get top charts
top_games = scraper.list_get_fields("TOP_FREE", "GAME", ["title", "score"], count=20, lang="en", country="us")
print(f"Top free game: {top_games[0]['title']} ({top_games[0]['score']}★)")

# Get similar apps
similar_apps = scraper.similar_get_fields(app_id, ["title", "score"], count=30, lang="en", country="us")
print(f"Similar app example: {similar_apps[0]['title']}")

# Get search suggestions
suggestions = scraper.suggest_analyze("fitness", count=5, lang="en", country="us")
print(suggestions)
```

Proxy configuration accepts either a single URL string (applied to both HTTP and
HTTPS traffic) or a dictionary mapping schemes to individual proxy URLs as shown
above.

## 🎯 7 Method Types

GPlay Scraper provides 7 method types with 20 helper functions to interact with Google Play Store data:

### 1. [App Methods](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/APP_METHODS.md) - Extract app details (65+ fields)
### 2. [Search Methods](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/SEARCH_METHODS.md) - Search for apps by keyword
### 3. [Reviews Methods](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/REVIEWS_METHODS.md) - Get user reviews and ratings
### 4. [Developer Methods](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/DEVELOPER_METHODS.md) - Get all apps from a developer
### 5. [List Methods](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/LIST_METHODS.md) - Get top charts (free, paid, grossing)
### 6. [Similar Methods](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/SIMILAR_METHODS.md) - Find similar/related apps
### 7. [Suggest Methods](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/SUGGEST_METHODS.md) - Get search suggestions/autocomplete

Each method type exposes three core functions:
- `analyze()` - Get all data as dictionary/list
- `get_field()` - Get single field value
- `get_fields()` - Get multiple fields

Suggest methods additionally offer `nested()` for second-level suggestions.

## 🎯 Method Examples

### 1. [App Methods](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/APP_METHODS.md) - Get App Details
Extract comprehensive information about any app including ratings, installs, pricing, and 65+ data fields.

📖 **[View detailed documentation →](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/APP_METHODS.md)**

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

# Analyze app data and print selected fields
data = scraper.app_analyze("com.whatsapp", lang="en", country="us")
print(f"{data['title']} — {data['score']} stars")
fields = scraper.app_get_fields("com.whatsapp", ["title", "installs", "free"], lang="en", country="us")
print(f"{fields['title']} — {fields['installs']} installs — {'Free' if fields['free'] else 'Paid'}")
```

**What you get:** Complete app profile with title, developer, ratings, install counts, pricing, screenshots, permissions, and more.

📄 **[View JSON example →](https://github.com/Mohammedcha/gplay-scraper/blob/main/output/app_example.json)**

---

### 2. [Search Methods](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/SEARCH_METHODS.md) - Find Apps by Keyword
Search the Play Store by keyword, app name, or category to discover apps.

📖 **[View detailed documentation →](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/SEARCH_METHODS.md)**

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

# Print selected details from search results
results = scraper.search_get_fields("fitness tracker", ["title", "developer"], count=20, lang="en", country="us")
for app in results[:5]:
    print(f"{app['title']} by {app['developer']}")
```

**What you get:** List of apps matching your search with titles, developers, ratings, prices, and Play Store URLs.

📄 **[View JSON example →](https://github.com/Mohammedcha/gplay-scraper/blob/main/output/search_example.json)**

---

### 3. [Reviews Methods](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/REVIEWS_METHODS.md) - Extract User Reviews
Get user reviews with ratings, comments, timestamps, and helpful votes for sentiment analysis.

📖 **[View detailed documentation →](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/REVIEWS_METHODS.md)**

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

# Print reviewer names and scores
reviews = scraper.reviews_get_fields("com.whatsapp", ["userName", "score"], count=100, sort="NEWEST", lang="en", country="us")
for review in reviews[:5]:
    print(f"{review['userName']}: {review['score']}★")
```

**What you get:** User reviews with names, ratings (1-5 stars), review text, timestamps, app versions, and helpful vote counts.

📄 **[View JSON example →](https://github.com/Mohammedcha/gplay-scraper/blob/main/output/reviews_example.json)**

---

### 4. [Developer Methods](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/DEVELOPER_METHODS.md) - Get Developer's Apps
Retrieve all apps published by a specific developer using their developer ID.

📖 **[View detailed documentation →](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/DEVELOPER_METHODS.md)**

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

# Print portfolio summary
portfolio = scraper.developer_get_fields("5700313618786177705", ["title", "score"], count=50, lang="en", country="us")
for app in portfolio[:5]:
    print(f"{app['title']}: {app['score']}★")
```

**What you get:** Complete portfolio of apps from a developer with titles, ratings, prices, and descriptions.

📄 **[View JSON example →](https://github.com/Mohammedcha/gplay-scraper/blob/main/output/developer_example.json)**

---

### 5. [List Methods](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/LIST_METHODS.md) - Get Top Charts
Access Play Store top charts including top free, top paid, and top grossing apps by category.

📖 **[View detailed documentation →](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/LIST_METHODS.md)**

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

# Print top free games summary
top_free_games = scraper.list_get_fields("TOP_FREE", "GAME", ["title", "score"], count=50, lang="en", country="us")
for app in top_free_games[:5]:
    print(f"{app['title']}: {app['score']}★")
```

**What you get:** Top-ranked apps with titles, developers, ratings, install counts, prices, and screenshots.

📄 **[View JSON example →](https://github.com/Mohammedcha/gplay-scraper/blob/main/output/list_example.json)**

---

### 6. [Similar Methods](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/SIMILAR_METHODS.md) - Find Related Apps
Discover apps similar to a reference app for competitive analysis and market research.

📖 **[View detailed documentation →](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/SIMILAR_METHODS.md)**

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

# Print similar apps summary
similar_apps = scraper.similar_get_fields("com.whatsapp", ["title", "score"], count=30, lang="en", country="us")
for app in similar_apps[:5]:
    print(f"{app['title']}: {app['score']}★")
```

**What you get:** List of similar/competitor apps with titles, developers, ratings, and pricing information.

📄 **[View JSON example →](https://github.com/Mohammedcha/gplay-scraper/blob/main/output/similar_example.json)**

---

### 7. [Suggest Methods](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/SUGGEST_METHODS.md) - Get Search Suggestions
Get autocomplete suggestions and keyword ideas for ASO and market research.

📖 **[View detailed documentation →](https://github.com/Mohammedcha/gplay-scraper/blob/main/README/SUGGEST_METHODS.md)**

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

# Print nested search suggestions
nested = scraper.suggest_nested("photo editor", count=10, lang="en", country="us")
for seed, suggestions in list(nested.items())[:3]:
    print(f"{seed}: {', '.join(suggestions[:3])}")
```

**What you get:** List of popular search terms related to your keyword for ASO and keyword research.

📄 **[View JSON example →](https://github.com/Mohammedcha/gplay-scraper/blob/main/output/suggest_example.json)**

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Happy Analyzing! 🚀**
