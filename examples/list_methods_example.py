"""
List Methods Example
Demonstrates all 6 list methods for getting top charts

Parameters:
- collection: Chart type - 'TOP_FREE', 'TOP_PAID', 'TOP_GROSSING' (default: 'TOP_FREE')
- category: Category filter (default: 'APPLICATION')
- count: Number of apps (default: 100)
- lang: Language code (default: 'en')
- country: Country code (default: 'us')
"""

from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
collection = "TOP_FREE"
category = "GAME"
count = 20
lang = "en"
country = "us"

print("=== List Methods Example ===\n")

# 1. list_analyze() - Get all top chart apps
print("1. list_analyze(collection='TOP_FREE', category='APPLICATION', count=100, lang='en', country='us')")
apps = scraper.list_analyze(collection, category, count=count, lang=lang, country=country)
print(f"   Found {len(apps)} apps")
print(f"   First app: {apps[0]['title']}")

# 2. list_get_field() - Get single field from all apps
print("\n2. list_get_field(collection, field, category='APPLICATION', count=100, lang='en', country='us')")
titles = scraper.list_get_field(collection, "title", category, count=count, lang=lang, country=country)
print(f"   Titles: {titles[:3]}")

# 3. list_get_fields() - Get multiple fields from all apps
print("\n3. list_get_fields(collection, fields, category='APPLICATION', count=100, lang='en', country='us')")
apps_data = scraper.list_get_fields(collection, ["title", "score"], category, count=10, lang=lang, country=country)
print(f"   First 2 apps: {apps_data[:2]}")

# 4. list_print_field() - Print single field from all apps
print("\n4. list_print_field(collection, field, category='APPLICATION', count=100, lang='en', country='us')")
scraper.list_print_field(collection, "title", category, count=5, lang=lang, country=country)

# 5. list_print_fields() - Print multiple fields from all apps
print("\n5. list_print_fields(collection, fields, category='APPLICATION', count=100, lang='en', country='us')")
scraper.list_print_fields(collection, ["title", "score"], category, count=5, lang=lang, country=country)

# 6. list_print_all() - Print all top chart apps as JSON
print("\n6. list_print_all(collection='TOP_FREE', category='APPLICATION', count=100, lang='en', country='us')")
scraper.list_print_all(collection, category, count=5, lang=lang, country=country)
