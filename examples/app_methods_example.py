"""
App Methods Example
Demonstrates all 6 app methods for extracting app details

Parameters:
- app_id: App package name
- lang: Language code (default: 'en')
- country: Country code (default: 'us')
"""

from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
app_id = "com.whatsapp"
lang = "en"
country = "us"

print("=== App Methods Example ===\n")

# 1. app_analyze() - Get all data as dictionary
print("1. app_analyze(app_id, lang='en', country='us')")
data = scraper.app_analyze(app_id, lang=lang, country=country)
print(f"   Retrieved {len(data)} fields")
print(f"   Title: {data['title']}")
print(f"   Score: {data['score']}")

# 2. app_get_field() - Get single field
print("\n2. app_get_field(app_id, field, lang='en', country='us')")
title = scraper.app_get_field(app_id, "title", lang=lang, country=country)
print(f"   Title: {title}")

# 3. app_get_fields() - Get multiple fields
print("\n3. app_get_fields(app_id, fields, lang='en', country='us')")
fields = scraper.app_get_fields(app_id, ["title", "score", "installs"], lang=lang, country=country)
print(f"   {fields}")

# 4. app_print_field() - Print single field
print("\n4. app_print_field(app_id, field, lang='en', country='us')")
scraper.app_print_field(app_id, "developer", lang=lang, country=country)

# 5. app_print_fields() - Print multiple fields
print("\n5. app_print_fields(app_id, fields, lang='en', country='us')")
scraper.app_print_fields(app_id, ["title", "score", "free"], lang=lang, country=country)

# 6. app_print_all() - Print all data as JSON
print("\n6. app_print_all(app_id, lang='en', country='us')")
scraper.app_print_all(app_id, lang=lang, country=country)
