"""
Suggest Methods Example
Demonstrates all 4 suggest methods for getting search suggestions

Parameters:
- term: Search term
- count: Number of suggestions (default: 5)
- lang: Language code (default: 'en')
- country: Country code (default: 'us')
"""

from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
term = "fitness"
count = 5
lang = "en"
country = "us"

print("=== Suggest Methods Example ===\n")

# 1. suggest_analyze() - Get search suggestions
print("1. suggest_analyze(term, count=5, lang='en', country='us')")
suggestions = scraper.suggest_analyze(term, count=count, lang=lang, country=country)
print(f"   Suggestions: {suggestions}")

# 2. suggest_nested() - Get nested suggestions
print("\n2. suggest_nested(term, count=5, lang='en', country='us')")
nested = scraper.suggest_nested(term, count=count, lang=lang, country=country)
print(f"   Nested suggestions (first 2):")
for i, (key, values) in enumerate(list(nested.items())[:2]):
    print(f"   {key}: {values}")

# 3. suggest_print_all() - Print suggestions as JSON
print("\n3. suggest_print_all(term, count=5, lang='en', country='us')")
scraper.suggest_print_all(term, count=count, lang=lang, country=country)

# 4. suggest_print_nested() - Print nested suggestions as JSON
print("\n4. suggest_print_nested(term, count=5, lang='en', country='us')")
scraper.suggest_print_nested(term, count=count, lang=lang, country=country)
