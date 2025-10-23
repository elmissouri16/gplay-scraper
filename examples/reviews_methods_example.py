"""
Reviews Methods Example
Demonstrates the core reviews helpers for extracting and formatting user feedback.

Parameters:
- app_id: App package name
- count: Number of reviews (default: 100)
- lang: Language code (default: 'en')
- country: Country code (default: 'us')
- sort: Sort order - 'NEWEST', 'RELEVANT', 'RATING' (default: 'NEWEST')
"""

from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
app_id = "com.whatsapp"
count = 20
lang = "en"
country = "us"
sort = "NEWEST"

print("=== Reviews Methods Example ===\n")

# 1. reviews_analyze() - Get all reviews
print("1. reviews_analyze(app_id, count=100, lang='en', country='us', sort='NEWEST')")
reviews = scraper.reviews_analyze(app_id, count=count, lang=lang, country=country, sort=sort)
print(f"   Retrieved {len(reviews)} reviews")
print(f"   First review score: {reviews[0]['score']}")

# 2. reviews_get_field() - Get single field from all reviews
print("\n2. reviews_get_field(app_id, field, count=100, lang='en', country='us', sort='NEWEST')")
scores = scraper.reviews_get_field(app_id, "score", count=count, lang=lang, country=country, sort=sort)
print(f"   Scores: {scores[:5]}")

# 3. reviews_get_fields() - Get multiple fields from all reviews
print("\n3. reviews_get_fields(app_id, fields, count=100, lang='en', country='us', sort='NEWEST')")
review_data = scraper.reviews_get_fields(app_id, ["userName", "score"], count=10, lang=lang, country=country, sort=sort)
print(f"   First 2 reviews: {review_data[:2]}")

# 4. Display first five review scores
print("\n4. Display first five review scores using reviews_get_field")
for idx, score in enumerate(scores[:5], 1):
    print(f"   {idx}. {score}")

# 5. Display first five reviewer names and scores
print("\n5. Display first five reviewers with scores")
for idx, review in enumerate(review_data[:5], 1):
    print(f"   {idx}. {review.get('userName', 'Anonymous')} — {review.get('score', 'N/A')}★")
