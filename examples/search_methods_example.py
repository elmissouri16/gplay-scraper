"""
Search Methods Example
Demonstrates all 6 search methods for finding apps

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

# 4. search_print_field() - Print single field from all results
print("\n4. search_print_field(query, field, count=100, lang='en', country='us')")
scraper.search_print_field(query, "title", count=5, lang=lang, country=country)

# 5. search_print_fields() - Print multiple fields from all results
print("\n5. search_print_fields(query, fields, count=100, lang='en', country='us')")
scraper.search_print_fields(query, ["title", "developer"], count=5, lang=lang, country=country)

# 6. search_print_all() - Print all search results as JSON
print("\n6. search_print_all(query, count=100, lang='en', country='us')")
scraper.search_print_all(query, count=5, lang=lang, country=country)
