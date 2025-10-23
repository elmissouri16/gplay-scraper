# GPlay Scraper Documentation

GPlay Scraper is a Python library for extracting rich app data, reviews, and market intelligence from the Google Play Store without API keys. The library exposes 7 method families and 30+ convenience helpers to cover discovery, competitive research, and monitoring workflows.

![GPlay Scraper](https://github.com/Mohammedcha/gplay-scraper/blob/main/assets/gplay-scraper.png)

## Key Capabilities

- **7 method types** covering apps, search, reviews, developers, lists, similar, and suggestions.
- **65+ data fields** including installs, pricing, media assets, permissions, and data safety info.
- **curl_cffi-only HTTP backend** that impersonates Chrome for resilient scraping.
- **Regional controls** for more than 100 languages and 150 countries.
- **Type hints and dataclasses** for predictable outputs and IDE completion.

## Quick Start

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()

# App methods
app_data = scraper.app_analyze("com.whatsapp", lang="en", country="us")
print(app_data["title"])

# Search methods
top_apps = scraper.search_get_fields("productivity apps", ["title", "developer"], count=10, lang="en", country="us")
print(top_apps[:3])

# Reviews methods
scraper.reviews_print_fields("com.whatsapp", ["userName", "score"], count=10, sort="NEWEST")
```

## Documentation Map

- [Installation](installation.md)
- [Quick Start Guide](quickstart.md)
- [HTTP Client Details](http_client.md)
- [Fields Reference](fields_reference.md)
- [Configuration Guide](configuration.md)
- [Usage Examples](examples.md)
- [API Reference](api_reference.md)
- [Changelog](../CHANGELOG.md)
- [Contribution Guide](../CONTRIBUTING.md)
- [License](../LICENSE)

The repository also includes detailed breakdowns for each method family in the [`README/`](../README/README.md) directory:

- [App Methods](../README/APP_METHODS.md)
- [Search Methods](../README/SEARCH_METHODS.md)
- [Reviews Methods](../README/REVIEWS_METHODS.md)
- [Developer Methods](../README/DEVELOPER_METHODS.md)
- [List Methods](../README/LIST_METHODS.md)
- [Similar Methods](../README/SIMILAR_METHODS.md)
- [Suggest Methods](../README/SUGGEST_METHODS.md)

## Need Help?

- Use the examples to bootstrap scripts quickly.
- File issues or feature requests on [GitHub](https://github.com/Mohammedcha/gplay-scraper/issues).
- Join discussions in repository issues to share ideas or troubleshooting tips.
