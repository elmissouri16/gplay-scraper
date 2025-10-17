"""
Similar Methods Example
Demonstrates all 6 similar methods for finding related apps

Parameters:
- app_id: App package name
- count: Number of similar apps (default: 100)
- lang: Language code (default: 'en')
- country: Country code (default: 'us')
"""

from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
app_id = "com.whatsapp"
count = 20
lang = "en"
country = "us"

print("=== Similar Methods Example ===\n")

# 1. similar_analyze() - Get all similar apps
print("1. similar_analyze(app_id, count=100, lang='en', country='us')")
apps = scraper.similar_analyze(app_id, count=count, lang=lang, country=country)
print(f"   Found {len(apps)} similar apps")
print(f"   First app: {apps[0]['title']}")

# 2. similar_get_field() - Get single field from all similar apps
print("\n2. similar_get_field(app_id, field, count=100, lang='en', country='us')")
titles = scraper.similar_get_field(app_id, "title", count=count, lang=lang, country=country)
print(f"   Titles: {titles[:3]}")

# 3. similar_get_fields() - Get multiple fields from all similar apps
print("\n3. similar_get_fields(app_id, fields, count=100, lang='en', country='us')")
apps_data = scraper.similar_get_fields(app_id, ["title", "score"], count=10, lang=lang, country=country)
print(f"   First 2 apps: {apps_data[:2]}")

# 4. similar_print_field() - Print single field from all similar apps
print("\n4. similar_print_field(app_id, field, count=100, lang='en', country='us')")
scraper.similar_print_field(app_id, "title", count=5, lang=lang, country=country)

# 5. similar_print_fields() - Print multiple fields from all similar apps
print("\n5. similar_print_fields(app_id, fields, count=100, lang='en', country='us')")
scraper.similar_print_fields(app_id, ["title", "score"], count=5, lang=lang, country=country)

# 6. similar_print_all() - Print all similar apps as JSON
print("\n6. similar_print_all(app_id, count=100, lang='en', country='us')")
scraper.similar_print_all(app_id, count=5, lang=lang, country=country)
