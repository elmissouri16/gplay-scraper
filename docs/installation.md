# Installation

## Requirements

- Python 3.7 or newer
- `curl-cffi` (installed automatically via `pip install gplay-scraper`)

## Install from PyPI

```bash
pip install gplay-scraper
```

## Development Installation

```bash
git clone https://github.com/mohammedcha/gplay-scraper.git
cd gplay-scraper
pip install -e .
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

- **HTTP client mismatch** – GPlay Scraper standardises on `curl_cffi`. Initialising `GPlayScraper()` uses this backend automatically and passing any other `http_client` value raises `ValueError`.

- **Common parameters** – All methods accept `lang`, `country`, and `count`.

  ```python
  scraper.app_print_all("com.whatsapp", lang="es", country="es")
  scraper.search_print_all("games", count=50, lang="en", country="us")
  ```
