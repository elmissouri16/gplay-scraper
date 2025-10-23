# GPlay Scraper Documentation

Complete documentation for all 7 method types in GPlay Scraper.

## 📚 Method Documentation

### [App Methods](APP_METHODS.md)
Extract comprehensive app data with 65+ fields including ratings, installs, pricing, screenshots, permissions, and technical details.

**Key Features:**
- 65+ data fields per app
- Basic info, ratings, installs, pricing
- Media content (screenshots, videos, icons)
- Technical specs (version, size, Android version)
- Developer information and contact details

**Use Cases:** App analysis, competitive research, market intelligence, data collection

---

### [Search Methods](SEARCH_METHODS.md)
Search Google Play Store apps by keyword with filtering and pagination.

**Key Features:**
- Search by keyword, app name, or category
- Filter and paginate results
- Get app titles, developers, ratings, prices
- Multi-language and multi-region support

**Use Cases:** App discovery, market research, competitor analysis, trend tracking

---

### [Reviews Methods](REVIEWS_METHODS.md)
Extract user reviews with ratings, timestamps, and detailed feedback for sentiment analysis.

**Key Features:**
- Get reviews with ratings (1-5 stars)
- Review text, timestamps, app versions
- Reviewer names and helpful vote counts
- Sort by newest, relevant, or highest rated

**Use Cases:** Sentiment analysis, user feedback, app improvement, competitive monitoring

---

### [Developer Methods](DEVELOPER_METHODS.md)
Get all apps published by a specific developer using their developer ID.

**Key Features:**
- Complete app portfolio for any developer
- Track developer's app performance
- Analyze ratings and install counts
- Monitor developer's market presence

**Use Cases:** Developer research, portfolio analysis, competitive intelligence, market tracking

---

### [List Methods](LIST_METHODS.md)
Access Google Play Store top charts including top free, top paid, and top grossing apps by category.

**Key Features:**
- Top free, top paid, top grossing charts
- 54 categories (36 app + 18 game)
- Ranked lists with install counts and ratings
- Trending apps and market leaders

**Use Cases:** Market trends, category analysis, competitive benchmarking, app discovery

---

### [Similar Methods](SIMILAR_METHODS.md)
Find apps similar to a reference app for competitive analysis and market research.

**Key Features:**
- Discover competitor apps
- Find similar/related apps
- Get titles, developers, ratings, pricing
- Competitive analysis and positioning

**Use Cases:** Competitive analysis, market research, app discovery, positioning strategy

---

### [Suggest Methods](SUGGEST_METHODS.md)
Get search suggestions and autocomplete from Google Play Store for keyword discovery and ASO.

**Key Features:**
- Autocomplete suggestions
- Popular search terms
- Nested keyword discovery
- Multi-language support

**Use Cases:** Keyword research, ASO optimization, content strategy, market insights

---

## 🚀 Quick Start

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

# App Methods
scraper.app_print_fields("com.whatsapp", ["title", "score", "installs"])

# Search Methods
scraper.search_print_fields("fitness tracker", ["title", "developer"], count=20)

# Reviews Methods
scraper.reviews_print_fields("com.whatsapp", ["userName", "score"], count=100, sort="NEWEST")

# Developer Methods
scraper.developer_print_fields("5700313618786177705", ["title", "score"], count=50)

# List Methods
scraper.list_print_fields("TOP_FREE", "GAME", ["title", "score"], count=50)

# Similar Methods
scraper.similar_print_fields("com.whatsapp", ["title", "score"], count=30)

# Suggest Methods
scraper.suggest_print_nested("photo editor", count=10)
```

## 📖 Method Pattern

Each method type follows the same pattern with 5 functions:

- **`analyze()`** - Get all data as dictionary/list
- **`get_field()`** - Get single field value
- **`get_fields()`** - Get multiple fields as dictionary
- **`print_field()`** - Print single field to console
- **`print_fields()`** - Print multiple fields to console
Suggest methods additionally expose `nested()` / `print_nested()`.

## 🌍 Multi-Language & Multi-Region

All methods support multi-language and multi-region parameters:

```python
# Get data in Spanish from Spain
scraper.app_analyze("com.whatsapp", lang="es", country="es")

# Get data in Japanese from Japan
scraper.search_analyze("game", count=20, lang="ja", country="jp")

# Get data in French from France
scraper.reviews_analyze("com.whatsapp", count=50, lang="fr", country="fr")
```

**Supported:**
- **Languages:** 100+ (en, es, fr, de, ja, ko, zh, ar, pt, ru, etc.)
- **Countries:** 150+ (us, gb, ca, au, in, br, jp, kr, de, fr, etc.)

## 🔧 HTTP Client

GPlay Scraper now relies exclusively on [`curl_cffi`](https://github.com/yifeikong/curl_cffi) with built-in Chrome impersonation. Initialising `GPlayScraper()` without arguments uses this client automatically; there is no override parameter for alternate HTTP clients.

## 📊 What Can You Scrape?

### App Data (65+ Fields)
- Basic: title, developer, description, category, genre
- Ratings: score, ratings count, histogram
- Installs: install count ranges, statistics
- Pricing: free/paid, price, in-app purchases
- Media: icon, screenshots, video, header image
- Technical: version, size, Android version, dates
- Content: age rating, privacy policy, contact info
- Features: permissions, what's new, website

### Search & Discovery
- Search apps by keyword
- Get search suggestions
- Find similar/competitor apps
- Access top charts by category

### Developer Intelligence
- Complete app portfolio
- Performance tracking
- Market presence analysis

### User Reviews
- Reviews with ratings and text
- Timestamps and app versions
- Reviewer names and votes
- Filter by sort options

### Market Research
- Multi-language support (100+ languages)
- Multi-region data (150+ countries)
- Localized pricing and availability
- Competitive analysis

## 🎯 Use Cases

**Market Research**
- Analyze competitor apps
- Track market trends
- Identify opportunities
- Benchmark performance

**App Development**
- Monitor user feedback
- Track app performance
- Analyze competitors
- Optimize app store presence

**Data Analysis**
- Collect app data for research
- Sentiment analysis from reviews
- Market intelligence reports
- Machine learning datasets

**Business Intelligence**
- Competitive monitoring
- Market positioning
- Trend analysis
- Strategic planning

## 📄 License

This project is licensed under the MIT License.

---

**For detailed documentation on each method type, click the links above.**
