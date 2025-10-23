# Suggest Methods

Get search suggestions and autocomplete from Google Play Store for keyword discovery and ASO.

## Quick Start

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

# Get suggestions
suggestions = scraper.suggest_analyze("video", count=5)
print(suggestions)
# ['video player', 'video editor', 'video downloader', 'video maker', 'video call']

# Get nested suggestions
nested = scraper.suggest_nested("video", count=3)
for term, suggestions in nested.items():
    print(f"{term}: {suggestions}")
```

---

## HTTP Client

GPlay Scraper now relies exclusively on [`curl_cffi`](https://github.com/yifeikong/curl_cffi) with a Chrome fingerprint. Initialising `GPlayScraper()` without arguments uses this client automatically; overriding the HTTP backend is not supported.

---

## Methods

### `suggest_analyze(term, count=5, lang='en', country='us')`
Returns search suggestions as a list of strings.

```python
suggestions = scraper.suggest_analyze("video", count=5)
# Returns: ['video player', 'video editor', 'video downloader', 'video maker', 'video call']
```

### `suggest_nested(term, count=5, lang='en', country='us')`
Returns nested suggestions (suggestions for each suggestion).

```python
nested = scraper.suggest_nested("video", count=3)
# Returns: {
#   'video player': ['video player hd', 'video player all format', 'video player pro'],
#   'video editor': ['video editor pro', 'video editor free', 'video editor app'],
#   'video downloader': ['video downloader for facebook', 'video downloader hd', ...]
# }
```

### `suggest_print_nested(term, count=5, lang='en', country='us')`
Prints nested suggestions as formatted JSON.

```python
scraper.suggest_print_nested("video", count=3)
# Output: Full JSON object with nested suggestions
```

---

## Return Formats

### Simple Suggestions (List)
```python
['video player', 'video editor', 'video downloader', 'video maker', 'video call']
```

### Nested Suggestions (Dictionary)
```python
{
  'video player': ['video player hd', 'video player all format', 'video player pro'],
  'video editor': ['video editor pro', 'video editor free', 'video editor app'],
  'video downloader': ['video downloader for facebook', 'video downloader hd']
}
```

---

## Practical Examples

### Autocomplete Feature
```python
def autocomplete(user_input):
    """Provide autocomplete suggestions as user types"""
    if len(user_input) < 2:
        return []
    
    suggestions = scraper.suggest_analyze(user_input, count=10)
    return suggestions

# Usage
print(autocomplete("gam"))  # ['game', 'games', 'gaming', ...]
print(autocomplete("photo"))  # ['photo editor', 'photo collage', ...]
```

### Keyword Research
```python
base_keywords = ["fitness", "workout", "exercise"]
all_keywords = set()

for keyword in base_keywords:
    suggestions = scraper.suggest_analyze(keyword, count=10)
    all_keywords.update(suggestions)
    print(f"{keyword}: {len(suggestions)} suggestions")

print(f"\nTotal unique keywords: {len(all_keywords)}")
print("Sample keywords:", list(all_keywords)[:10])
```

### Deep Keyword Mining
```python
term = "photo editor"
nested = scraper.suggest_nested(term, count=5)

print(f"Keyword tree for '{term}':")
for parent, children in nested.items():
    print(f"\n{parent}:")
    for child in children:
        print(f"  - {child}")
```

### ASO Keyword Discovery
```python
import json

def discover_keywords(seed_term, depth=2):
    """Discover keywords with specified depth"""
    keywords = {}
    
    # Level 1
    level1 = scraper.suggest_analyze(seed_term, count=10)
    keywords[seed_term] = level1
    
    if depth > 1:
        # Level 2
        for term in level1[:5]:  # Limit to avoid too many requests
            level2 = scraper.suggest_analyze(term, count=5)
            keywords[term] = level2
    
    return keywords

keywords = discover_keywords("game", depth=2)
print(json.dumps(keywords, indent=2))
```

### Trending Search Terms
```python
categories = ["game", "social", "productivity", "photo", "music"]
trending = {}

for category in categories:
    suggestions = scraper.suggest_analyze(category, count=5)
    trending[category] = suggestions
    print(f"{category}: {', '.join(suggestions[:3])}...")
```

### Long-Tail Keywords
```python
short_term = "vpn"
suggestions = scraper.suggest_analyze(short_term, count=10)

# Filter for long-tail (3+ words)
long_tail = [s for s in suggestions if len(s.split()) >= 3]

print(f"Long-tail keywords for '{short_term}':")
for keyword in long_tail:
    print(f"- {keyword}")
```

### Competitor Keyword Analysis
```python
competitor_apps = ["whatsapp", "telegram", "signal"]
all_suggestions = {}

for app in competitor_apps:
    suggestions = scraper.suggest_analyze(app, count=10)
    all_suggestions[app] = suggestions
    print(f"{app}: {len(suggestions)} suggestions")

# Find common keywords
common = set(all_suggestions[competitor_apps[0]])
for app in competitor_apps[1:]:
    common &= set(all_suggestions[app])

print(f"\nCommon keywords: {common}")
```

### Export Keyword Map
```python
import json

term = "fitness"
nested = scraper.suggest_nested(term, count=10)

with open(f'keywords_{term}.json', 'w') as f:
    json.dump(nested, f, indent=2)

print(f"Exported keyword map for '{term}'")
print(f"Total parent keywords: {len(nested)}")
print(f"Total child keywords: {sum(len(v) for v in nested.values())}")
```

### Search Volume Estimation
```python
term = "photo editor"
suggestions = scraper.suggest_analyze(term, count=20)

# Suggestions appear in order of popularity (roughly)
print(f"Top suggestions for '{term}' (by estimated popularity):")
for i, suggestion in enumerate(suggestions[:10], 1):
    print(f"{i}. {suggestion}")
```

---

## Parameters

### Initialization

### Method Parameters
- `term` (str, required) - Search term or keyword
- `count` (int, optional) - Number of suggestions to return (default: 5, max: ~10)
- `lang` (str, optional) - Language code (default: 'en')
- `country` (str, optional) - Country code (default: 'us')

### Search Term Tips
- Use partial words: "gam" → "game", "games", "gaming"
- Try categories: "fitness", "photo", "music"
- Test variations: "vpn", "vpn free", "vpn app"
- Use brand names: "whatsapp", "instagram"
- Combine terms: "photo editor free"

### Language & Country Codes
- **Language**: 'en', 'es', 'fr', 'de', 'ja', 'ko', 'pt', 'ru', 'zh', etc.
- **Country**: 'us', 'gb', 'ca', 'au', 'in', 'br', 'jp', 'kr', 'de', 'fr', etc.

---

## When to Use Each Method

- **`suggest_analyze()`** - Get simple list of suggestions for autocomplete or keyword research
- **`suggest_nested()`** - Deep keyword mining with two levels of suggestions
- **`suggest_print_nested()`** - Quick debugging/console output of nested suggestions
- **`suggest_print_nested()`** - Quick debugging/console output of nested suggestions

---

## Use Cases

### App Store Optimization (ASO)
- Discover high-traffic keywords
- Find long-tail keyword opportunities
- Analyze competitor keywords
- Optimize app title and description

### Market Research
- Identify trending search terms
- Understand user search behavior
- Discover niche markets
- Track keyword trends over time

### Content Strategy
- Generate content ideas
- Find related topics
- Optimize metadata
- Improve discoverability

### Competitive Analysis
- Discover competitor keywords
- Find keyword gaps
- Identify market opportunities
- Track competitor positioning

---

## Advanced Features

### Rate Limiting
Built-in rate limiting (1 second delay between requests) prevents blocking.

### Error Handling
```python
from gplay_scraper import GPlayScraper, NetworkError

scraper = GPlayScraper()

try:
    suggestions = scraper.suggest_analyze("")
except ValueError:
    print("Term cannot be empty")
except NetworkError:
    print("Network error occurred")
```

### Multi-Region Suggestions
```python
# Get suggestions from different regions
us_suggestions = scraper.suggest_analyze("game", country="us")
uk_suggestions = scraper.suggest_analyze("game", country="gb")
jp_suggestions = scraper.suggest_analyze("game", country="jp", lang="ja")

print(f"US: {us_suggestions[:3]}")
print(f"UK: {uk_suggestions[:3]}")
print(f"JP: {jp_suggestions[:3]}")
```

### Batch Processing
```python
terms = ["fitness", "diet", "workout", "yoga", "meditation"]
all_suggestions = {}

for term in terms:
    suggestions = scraper.suggest_analyze(term, count=10)
    all_suggestions[term] = suggestions
    print(f"{term}: {len(suggestions)} suggestions")

# Find overlapping keywords
all_keywords = set()
for suggestions in all_suggestions.values():
    all_keywords.update(suggestions)

print(f"\nTotal unique keywords: {len(all_keywords)}")
```

### Recursive Keyword Expansion
```python
def expand_keywords(term, max_depth=2, current_depth=0):
    """Recursively expand keywords"""
    if current_depth >= max_depth:
        return []
    
    suggestions = scraper.suggest_analyze(term, count=5)
    all_keywords = suggestions.copy()
    
    if current_depth < max_depth - 1:
        for suggestion in suggestions[:2]:  # Limit to avoid explosion
            child_keywords = expand_keywords(suggestion, max_depth, current_depth + 1)
            all_keywords.extend(child_keywords)
    
    return all_keywords

keywords = expand_keywords("game", max_depth=2)
print(f"Expanded to {len(set(keywords))} unique keywords")
```

### Suggestion Filtering
```python
term = "game"
suggestions = scraper.suggest_analyze(term, count=20)

# Filter by length
short = [s for s in suggestions if len(s.split()) <= 2]
long = [s for s in suggestions if len(s.split()) > 2]

# Filter by keyword
free_games = [s for s in suggestions if 'free' in s.lower()]

print(f"Short keywords: {len(short)}")
print(f"Long keywords: {len(long)}")
print(f"Free games: {len(free_games)}")
```
