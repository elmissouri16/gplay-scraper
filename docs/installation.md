# Installation

## Requirements

- Python 3.7 or newer
- [`uv`](https://github.com/astral-sh/uv) 0.4+ (optional, recommended for contributors)

## Install from PyPI

```bash
pip install gplay-scraper
```

## Install with uv (Optional)

```bash
uv pip install gplay-scraper
```

## Development Installation

```bash
git clone https://github.com/mohammedcha/gplay-scraper.git
cd gplay-scraper
pip install -e .
# or, using uv:
uv pip install --editable .

# include dev extras for contributors
uv sync --extra dev
```

## Verify Your Setup

```python
from gplay_scraper import GPlayScraper

scraper = GPlayScraper()
data = scraper.app_analyze("com.whatsapp")
print(f"Success! Retrieved: {data['title']}")

title = scraper.app_get_field("com.whatsapp", "title")
print(f"Title preview: {title}")  # alternate smoke test
```

## Troubleshooting

- **Unicode errors on Windows**

  ```python
  import sys
  if sys.platform == "win32":
      sys.stdout.reconfigure(encoding="utf-8")
  ```

- **Proxy format** – Pass a single proxy string (applies to HTTP/HTTPS) or a mapping such as `{"http": "http://proxy", "https": "http://secure-proxy"}`; call `set_proxies(None)` to clear.

- **Common parameters** – All methods accept `lang`, `country`, and `count`.

  ```python
  summary = scraper.app_get_fields("com.whatsapp", ["title", "score"], lang="es", country="es")
  print(summary)
  results = scraper.search_get_fields("games", ["title", "developer"], count=50, lang="en", country="us")
  print(results[:3])
  ```
