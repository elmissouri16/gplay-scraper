# Reviews Methods

Extract user reviews from Google Play Store apps with ratings, content, and metadata.

## Quick Start

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

# Get reviews
reviews = scraper.reviews_analyze("com.whatsapp", count=100, sort="NEWEST")
for review in reviews[:5]:
    print(f"{review['userName']}: {review['score']}★")
    print(f"  {review['content'][:100]}...")

# Get specific fields
scores = scraper.reviews_get_field("com.whatsapp", "score", count=100)
print(f"Average: {sum(scores)/len(scores):.2f}★")

# Get multiple fields
reviews = scraper.reviews_get_fields("com.whatsapp", ["userName", "score", "content"], count=50)
print(reviews)
```

---

## HTTP Client

GPlay Scraper now relies exclusively on [`curl_cffi`](https://github.com/yifeikong/curl_cffi) with a Chrome fingerprint. Initialising `GPlayScraper()` without arguments uses this client automatically; overriding the HTTP backend is not supported.

---

## Methods

### `reviews_analyze(app_id, count=100, lang='en', country='us', sort='NEWEST')`
Returns reviews as a list of dictionaries.

```python
reviews = scraper.reviews_analyze("com.whatsapp", count=100, sort="NEWEST")
# Returns: [{'reviewId': '...', 'userName': '...', 'score': 5, 'content': '...', ...}, ...]
```

### `reviews_get_field(app_id, field, count=100, lang='en', country='us', sort='NEWEST')`
Returns a specific field from all reviews.

```python
scores = scraper.reviews_get_field("com.whatsapp", "score", count=100)
# Returns: [5, 4, 5, 3, 4, ...]
```

### `reviews_get_fields(app_id, fields, count=100, lang='en', country='us', sort='NEWEST')`
Returns multiple fields from all reviews.

```python
reviews = scraper.reviews_get_fields("com.whatsapp", ["userName", "score", "content"], count=50)
# Returns: [{'userName': 'John', 'score': 5, 'content': 'Great app!'}, ...]
```

### `reviews_print_field(app_id, field, count=100, lang='en', country='us', sort='NEWEST')`
Prints a specific field from all reviews.

```python
scraper.reviews_print_field("com.whatsapp", "content", count=20)
# Output:
# 1. content: Great app!
# 2. content: Love it
# 3. content: Needs improvement
```

### `reviews_print_fields(app_id, fields, count=100, lang='en', country='us', sort='NEWEST')`
Prints multiple fields from all reviews.

```python
scraper.reviews_print_fields("com.whatsapp", ["userName", "score"], count=20)
# Output:
# userName: John, score: 5
# userName: Jane, score: 4
```

## Available Fields

- `reviewId` - Unique review ID
- `userName` - Reviewer name
- `userImage` - Reviewer avatar URL
- `score` - Review rating (1-5 stars)
- `content` - Review text/comment
- `thumbsUpCount` - Number of helpful votes
- `appVersion` - App version reviewed
- `at` - Review timestamp (ISO 8601 format)

---

## Sort Options

- **`NEWEST`** (default) - Most recent reviews first
- **`RELEVANT`** - Most relevant/helpful reviews
- **`RATING`** - Sorted by rating (highest/lowest)

---

## Practical Examples

### Sentiment Analysis
```python
reviews = scraper.reviews_get_fields("com.whatsapp", ["score", "content"], count=200)

# Rating distribution
rating_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
for review in reviews:
    rating_dist[review['score']] += 1

print("Rating Distribution:")
for rating, count in rating_dist.items():
    print(f"{rating}★: {'█' * count} ({count})")

# Average rating
avg = sum(r['score'] for r in reviews) / len(reviews)
print(f"\nAverage: {avg:.2f}★")
```

### Find Common Issues
```python
reviews = scraper.reviews_get_fields("com.whatsapp", ["score", "content"], count=100, sort="RATING")

# Get low-rated reviews
low_rated = [r for r in reviews if r['score'] <= 2]

print(f"Found {len(low_rated)} low-rated reviews:")
for review in low_rated[:10]:
    print(f"- {review['content'][:100]}...")
```

### Track Review Trends
```python
from datetime import datetime

reviews = scraper.reviews_get_fields("com.whatsapp", ["at", "score"], count=500, sort="NEWEST")

# Group by month
monthly_scores = {}
for review in reviews:
    date = datetime.fromisoformat(review['at'])
    month_key = date.strftime("%Y-%m")
    
    if month_key not in monthly_scores:
        monthly_scores[month_key] = []
    monthly_scores[month_key].append(review['score'])

# Calculate monthly averages
for month, scores in sorted(monthly_scores.items()):
    avg = sum(scores) / len(scores)
    print(f"{month}: {avg:.2f}★ ({len(scores)} reviews)")
```

### Compare App Versions
```python
reviews = scraper.reviews_get_fields("com.whatsapp", ["appVersion", "score"], count=300)

# Group by version
version_scores = {}
for review in reviews:
    version = review['appVersion'] or "Unknown"
    if version not in version_scores:
        version_scores[version] = []
    version_scores[version].append(review['score'])

# Show version ratings
for version, scores in sorted(version_scores.items()):
    if len(scores) >= 5:  # Only versions with 5+ reviews
        avg = sum(scores) / len(scores)
        print(f"v{version}: {avg:.2f}★ ({len(scores)} reviews)")
```

### Export Reviews to CSV
```python
import csv

reviews = scraper.reviews_analyze("com.whatsapp", count=500)

with open('reviews.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['userName', 'score', 'content', 'at', 'appVersion'])
    writer.writeheader()
    
    for review in reviews:
        writer.writerow({
            'userName': review['userName'],
            'score': review['score'],
            'content': review['content'],
            'at': review['at'],
            'appVersion': review['appVersion']
        })

print(f"Exported {len(reviews)} reviews to reviews.csv")
```

### Identify Top Reviewers
```python
reviews = scraper.reviews_get_fields("com.whatsapp", ["userName", "thumbsUpCount"], count=200)

# Sort by helpful votes
top_reviewers = sorted(reviews, key=lambda x: x['thumbsUpCount'] or 0, reverse=True)[:10]

print("Top 10 Most Helpful Reviewers:")
for i, review in enumerate(top_reviewers, 1):
    print(f"{i}. {review['userName']}: {review['thumbsUpCount']} helpful votes")
```

### Monitor Recent Feedback
```python
import time
from datetime import datetime

def monitor_reviews(app_id, interval=3600):
    """Check for new reviews every hour"""
    last_check = datetime.now()
    
    while True:
        reviews = scraper.reviews_get_fields(app_id, ["at", "score", "content"], count=50, sort="NEWEST")
        
        new_reviews = [r for r in reviews if datetime.fromisoformat(r['at']) > last_check]
        
        if new_reviews:
            print(f"\n{len(new_reviews)} new reviews:")
            for review in new_reviews:
                print(f"- {review['score']}★: {review['content'][:80]}...")
        
        last_check = datetime.now()
        time.sleep(interval)

# Run monitor (Ctrl+C to stop)
# monitor_reviews("com.whatsapp")
```

### Keyword Analysis
```python
from collections import Counter
import re

reviews = scraper.reviews_get_field("com.whatsapp", "content", count=500)

# Extract words
words = []
for content in reviews:
    if content:
        words.extend(re.findall(r'\b\w+\b', content.lower()))

# Remove common words
stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'for'}
filtered_words = [w for w in words if w not in stop_words and len(w) > 3]

# Top keywords
top_keywords = Counter(filtered_words).most_common(20)
print("Top Keywords in Reviews:")
for word, count in top_keywords:
    print(f"{word}: {count}")
```

---

## Parameters

### Initialization

### Method Parameters
- `app_id` (str, required) - App package name
- `count` (int, optional) - Maximum number of reviews to return (default: 100)
- `lang` (str, optional) - Language code (default: 'en')
- `country` (str, optional) - Country code (default: 'us')
- `sort` (str, optional) - Sort order: "NEWEST", "RELEVANT", "RATING" (default: "NEWEST")
- `field` (str) - Single field name
- `fields` (List[str]) - List of field names

### Language & Country Codes
- **Language**: 'en', 'es', 'fr', 'de', 'ja', 'ko', 'pt', 'ru', 'zh', etc.
- **Country**: 'us', 'gb', 'ca', 'au', 'in', 'br', 'jp', 'kr', 'de', 'fr', etc.

---

## When to Use Each Method

- **`reviews_analyze()`** - Need complete review data for analysis
- **`reviews_get_field()`** - Need just one field (e.g., all scores)
- **`reviews_get_fields()`** - Need specific fields (more efficient)
- **`reviews_print_field()`** - Quick debugging/console output
- **`reviews_print_fields()`** - Quick debugging of multiple fields
- **`reviews_print_fields()`** - Explore available data structure

---

## Advanced Features

### Rate Limiting
Built-in rate limiting (1 second delay between requests) prevents blocking.

### Batch Fetching
Reviews are fetched in batches of 50. The library automatically handles pagination.

```python
# Fetch 500 reviews (10 batches of 50)
reviews = scraper.reviews_analyze("com.whatsapp", count=500)
print(f"Fetched {len(reviews)} reviews")
```

### Error Handling
```python
from gplay_scraper import GPlayScraper, AppNotFoundError, NetworkError

scraper = GPlayScraper()

try:
    reviews = scraper.reviews_analyze("invalid.app.id")
except AppNotFoundError:
    print("App not found")
except NetworkError:
    print("Network error occurred")
```

### Multi-Region Reviews
```python
# Get reviews from different regions
us_reviews = scraper.reviews_analyze("com.whatsapp", country="us", count=100)
uk_reviews = scraper.reviews_analyze("com.whatsapp", country="gb", count=100)
jp_reviews = scraper.reviews_analyze("com.whatsapp", country="jp", lang="ja", count=100)

print(f"US avg: {sum(r['score'] for r in us_reviews)/len(us_reviews):.2f}★")
print(f"UK avg: {sum(r['score'] for r in uk_reviews)/len(uk_reviews):.2f}★")
print(f"JP avg: {sum(r['score'] for r in jp_reviews)/len(jp_reviews):.2f}★")
```

### Sort Comparison
```python
# Compare different sort orders
newest = scraper.reviews_get_fields("com.whatsapp", ["score"], count=100, sort="NEWEST")
relevant = scraper.reviews_get_fields("com.whatsapp", ["score"], count=100, sort="RELEVANT")
rating = scraper.reviews_get_fields("com.whatsapp", ["score"], count=100, sort="RATING")

print(f"Newest avg: {sum(r['score'] for r in newest)/len(newest):.2f}★")
print(f"Relevant avg: {sum(r['score'] for r in relevant)/len(relevant):.2f}★")
print(f"Rating avg: {sum(r['score'] for r in rating)/len(rating):.2f}★")
```
