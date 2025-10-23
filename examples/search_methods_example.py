"""
Search Methods Example
Demonstrates the core search helpers for finding and formatting app results.

Parameters:
- query: Search keyword
- count: Number of results (default: 100)
- lang: Language code (default: 'en')
- country: Country code (default: 'us')
"""

from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
query = "social media"
count = 10
lang = "en"
country = "us"

print("=== Search Methods Example ===\n")

# 1. search_analyze() - Get all search results
print("1. search_analyze(query, count=100, lang='en', country='us')")
results = scraper.search_analyze(query, count=count, lang=lang, country=country)
print(f"   Found {len(results)} apps")
print(f"   First app: {results[0]['title']}")

# 2. search_get_field() - Get single field from all results
print("\n2. search_get_field(query, field, count=100, lang='en', country='us')")
titles = scraper.search_get_field(query, "title", count=count, lang=lang, country=country)
print(f"   Titles: {titles[:3]}")

# 3. search_get_fields() - Get multiple fields from all results
print("\n3. search_get_fields(query, fields, count=100, lang='en', country='us')")
apps = scraper.search_get_fields(query, ["title", "score"], count=count, lang=lang, country=country)
print(f"   First 2 apps: {apps[:2]}")

# 4. Display first five titles
print("\n4. Display first five titles from search_get_field")
for idx, title in enumerate(titles[:5], 1):
    print(f"   {idx}. {title}")

# 5. Display first five apps with title and developer
print("\n5. Display first five apps with title and developer")
for idx, app in enumerate(apps[:5], 1):
    print(f"   {idx}. {app.get('title', 'N/A')} — {app.get('developer', 'Unknown')}")
