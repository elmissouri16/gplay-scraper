# Installation

## Requirements

- Python 3.7 or newer
- `curl-cffi` is installed automatically with the package
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

scraper.app_print_all("com.whatsapp")  # alternate smoke test
```

## Troubleshooting

- **Unicode errors on Windows**

  ```python
  import sys
  if sys.platform == "win32":
      sys.stdout.reconfigure(encoding="utf-8")
  ```

- **HTTP client** – GPlay Scraper standardises on `curl_cffi`. Initialising `GPlayScraper()` uses this backend automatically and the client cannot be overridden.
- **Proxy format** – Pass a single proxy string (applies to HTTP/HTTPS) or a mapping such as `{"http": "http://proxy", "https": "http://secure-proxy"}`; call `set_proxies(None)` to clear.

- **Common parameters** – All methods accept `lang`, `country`, and `count`.

  ```python
  scraper.app_print_all("com.whatsapp", lang="es", country="es")
  scraper.search_print_all("games", count=50, lang="en", country="us")
  ```
