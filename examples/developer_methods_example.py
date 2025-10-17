"""
Developer Methods Example
Demonstrates all 6 developer methods for getting developer's apps

Parameters:
- dev_id: Developer ID (numeric or string)
- count: Number of apps (default: 100)
- lang: Language code (default: 'en')
- country: Country code (default: 'us')
"""

from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
dev_id = "5700313618786177705"  # Google LLC
count = 20
lang = "en"
country = "us"

print("=== Developer Methods Example ===\n")

# 1. developer_analyze() - Get all developer apps
print("1. developer_analyze(dev_id, count=100, lang='en', country='us')")
apps = scraper.developer_analyze(dev_id, count=count, lang=lang, country=country)
print(f"   Found {len(apps)} apps")
print(f"   First app: {apps[0]['title']}")

# 2. developer_get_field() - Get single field from all apps
print("\n2. developer_get_field(dev_id, field, count=100, lang='en', country='us')")
titles = scraper.developer_get_field(dev_id, "title", count=count, lang=lang, country=country)
print(f"   Titles: {titles[:3]}")

# 3. developer_get_fields() - Get multiple fields from all apps
print("\n3. developer_get_fields(dev_id, fields, count=100, lang='en', country='us')")
apps_data = scraper.developer_get_fields(dev_id, ["title", "score"], count=10, lang=lang, country=country)
print(f"   First 2 apps: {apps_data[:2]}")

# 4. developer_print_field() - Print single field from all apps
print("\n4. developer_print_field(dev_id, field, count=100, lang='en', country='us')")
scraper.developer_print_field(dev_id, "title", count=5, lang=lang, country=country)

# 5. developer_print_fields() - Print multiple fields from all apps
print("\n5. developer_print_fields(dev_id, fields, count=100, lang='en', country='us')")
scraper.developer_print_fields(dev_id, ["title", "score"], count=5, lang=lang, country=country)

# 6. developer_print_all() - Print all developer apps as JSON
print("\n6. developer_print_all(dev_id, count=100, lang='en', country='us')")
scraper.developer_print_all(dev_id, count=5, lang=lang, country=country)
