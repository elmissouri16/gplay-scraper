# API Reference

This page summarises the public surface of the library and links to the primary helpers you will use.

## Public Entry Points

### `gplay_scraper.GPlayScraper`

- Main facade class used in all examples.
- Provides 7 method families (`app_*`, `search_*`, `reviews_*`, `developer_*`, `list_*`, `similar_*`, `suggest_*`).
- Each family implements `analyze`, `get_field`, and `get_fields`.
- Optional parameters include `lang`, `country`, `count`, and `assets`.

See the dedicated guides in `README/`:

- [App Methods](../README/APP_METHODS.md)
- [Search Methods](../README/SEARCH_METHODS.md)
- [Reviews Methods](../README/REVIEWS_METHODS.md)
- [Developer Methods](../README/DEVELOPER_METHODS.md)
- [List Methods](../README/LIST_METHODS.md)
- [Similar Methods](../README/SIMILAR_METHODS.md)
- [Suggest Methods](../README/SUGGEST_METHODS.md)

### `gplay_scraper.Config`

- Exposes global configuration constants (`DEFAULT_TIMEOUT`, `RATE_LIMIT_DELAY`, etc.).
- Provides helpers such as `Config.get_headers(user_agent: str | None)` for consistent HTTP headers.

### Exceptions (`gplay_scraper.exceptions`)

- `AppNotFoundError`
- `ParseError`
- `NetworkError`
- `InvalidClientError`
- `TooManyRequestsError`
- `UnexpectedResponseError`

Catch these exceptions to deliver precise error handling in production scripts.

## Core Modules

- `gplay_scraper.core.gplay_methods` – Implements the seven method mixins used by `GPlayScraper`.
- `gplay_scraper.core.gplay_scraper` – Orchestrates fetching, caching, and rate limiting.
- `gplay_scraper.core.gplay_parser` – Parses Play Store payloads into structured dictionaries.
- `gplay_scraper.models` – Dataclasses and element specifications used throughout the parser.
- `gplay_scraper.utils.http_client` – Thin wrapper around `curl_cffi` providing retry and impersonation logic.
- `gplay_scraper.utils.helpers` – Utility functions for text cleaning, date parsing, and JSON post-processing.

## Formatting Helpers

Use `analyze()`, `get_field()`, and `get_fields()` to retrieve data, then format it with standard Python utilities such as `print()`, `json.dumps()`, or your preferred templating library.

## Versioning

Refer to the repository [changelog](../CHANGELOG.md) for release notes and API changes.
