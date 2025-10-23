# Configuration

GPlay Scraper offers several hooks for tuning performance, rate limits, and output.

## Default Settings

```python
from gplay_scraper import Config

print(f"Timeout: {Config.DEFAULT_TIMEOUT}s")            # 30 seconds
print(f"Rate limit: {Config.RATE_LIMIT_DELAY}s")        # 1.0 seconds
print(f"ASO keywords: {Config.ASO_TOP_KEYWORDS}")       # 20
print(f"Min word length: {Config.ASO_MIN_WORD_LENGTH}") # 3
```

## Network Configuration

### Timeout

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
print(f"Current timeout: {scraper.scraper.timeout}s")

scraper.scraper.timeout = 45  # applies to future requests
```

### Rate Limiting

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()                # default 1 second delay
scraper.scraper.rate_limit_delay = 2.0  # custom delay
scraper.scraper.rate_limit_delay = 0    # disable (not recommended)
```

### Proxies

```python
from gplay_scraper import GPlayScraper

# Single proxy string applies to both HTTP and HTTPS
scraper = GPlayScraper(proxies="http://127.0.0.1:8080")

# Provide a mapping to control schemes independently
scraper = GPlayScraper(
    proxies={
        "http": "socks5://127.0.0.1:9050",
        "https": "http://proxy.example.com:8443",
    }
)

# Update or clear proxies later
scraper.set_proxies(None)  # removes active proxies
```

### User Agent

```python
from gplay_scraper import Config

headers = Config.get_headers()             # curl_cffi sets a Chrome UA internally
custom = Config.get_headers("MyApp/1.0")   # only override if you must
print(custom["User-Agent"])
```

## ASO Configuration

### Keyword Analysis

```python
from gplay_scraper import GPlayScraper, Config

scraper = GPlayScraper()
data = scraper.analyze("com.hubolabs.hubo")

# Adjust keyword count (requires direct call)
scraper.aso_analyzer.analyze_app_text(data, top_n=50)
```

### Stop Words

```python
from gplay_scraper.core.aso_analyzer import AsoAnalyzer

analyzer = AsoAnalyzer()
print(f"Stop words count: {len(analyzer.default_stop_words)}")

custom_stop_words = analyzer.default_stop_words.copy()
custom_stop_words.update({"custom", "words", "to", "exclude"})

tokens = analyzer.tokenize_text("Your text here", stop_words=custom_stop_words)
```

## Caching

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
data1 = scraper.analyze("com.hubolabs.hubo")  # hits Play Store
data2 = scraper.analyze("com.hubolabs.hubo")  # served from cache

scraper._cache.clear()  # clear cache if required
```

## Environment Variables

```python
import os
from gplay_scraper import GPlayScraper

os.environ["GPLAY_TIMEOUT"] = "45"
os.environ["GPLAY_RATE_LIMIT"] = "2.0"

timeout = int(os.environ.get("GPLAY_TIMEOUT", 30))
rate_limit = float(os.environ.get("GPLAY_RATE_LIMIT", 1.0))

scraper = GPlayScraper()
scraper.scraper.timeout = timeout
scraper.scraper.rate_limit_delay = rate_limit
```

## Advanced Configuration

### Custom Request Tweaks

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
http_client = scraper.app_methods.scraper.http_client

http_client.timeout = 60
http_client.headers["Accept-Language"] = "en-US,en;q=0.9"
```

### Logging

```python
import logging
from gplay_scraper import GPlayScraper

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("gplay_scraper")

scraper = GPlayScraper()
data = scraper.analyze("com.hubolabs.hubo")
```

### Error Handling

```python
from gplay_scraper import GPlayScraper, AppNotFoundError, NetworkError

scraper = GPlayScraper()

try:
    data = scraper.app_analyze("com.whatsapp")
except AppNotFoundError:
    print("App not found")
except NetworkError:
    print("Network error occurred")
except Exception as exc:
    print(f"Unexpected error: {exc}")
```

## Method Selection Cheat Sheet

- **App Methods**
  - `app_analyze()` – full payload
  - `app_get_field()` – single field
  - `app_get_fields()` – subset of fields (format the result with standard Python utilities)

- **Search Methods**
  - `search_analyze()` – full search data
  - `search_get_field()` / `search_get_fields()` – targeted data (loop over returned values to display them)

- **Reviews Methods**
  - `reviews_analyze()` – detailed review data
  - `reviews_get_field()` / `reviews_get_fields()` – specific fields (iterate and format as needed)

- **Developer Methods**
  - `developer_analyze()` – full portfolio
  - `developer_get_field()` / `developer_get_fields()` – targeted fields (format using Python printing or JSON tooling)

- **List Methods**
  - `list_analyze()` – complete chart data
  - `list_get_field()` / `list_get_fields()` – specific fields (format the list for reporting)

- **Similar Methods**
  - `similar_analyze()` – related apps payload
  - `similar_get_field()` / `similar_get_fields()` – specific values (format for comparison dashboards)

- **Suggest Methods**
  - `suggest_analyze()` – suggestion list
  - `suggest_nested()` – recursive suggestions (pretty-print nested dicts manually)

## Best Practices

- **Rate limiting** – Keep at least a one second delay to avoid throttling.
- **Error handling** – Wrap scraper calls in try/except in production.
- **HTTP backend** – `curl_cffi` is mandatory; the client is fixed and non-configurable.
- **Use `get_fields()`** – Prefer batch getters over multiple `get_field()` calls.
- **Timeouts** – Adjust to match your network’s characteristics.
- **Logging** – Enable debug logs when diagnosing issues.
- **Localization** – Always set `lang` and `country` for the markets you analyse.
