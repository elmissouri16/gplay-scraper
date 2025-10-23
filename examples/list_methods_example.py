"""
List Methods Example
Demonstrates the core list helpers for exploring top charts data.

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

# 4. Display first five titles
print("\n4. Display first five titles from list_get_field")
for idx, title in enumerate(titles[:5], 1):
    print(f"   {idx}. {title}")

# 5. Display first five apps with title and score
print("\n5. Display first five apps with title and score")
for idx, app in enumerate(apps_data[:5], 1):
    print(f"   {idx}. {app.get('title', 'N/A')} — {app.get('score', 'N/A')}★")
