# HTTP Client

GPlay Scraper ships with a single HTTP backend: [`curl_cffi`](https://github.com/yifeikong/curl_cffi). The scraper establishes a Chrome-style session during initialisation, giving you modern TLS fingerprints and reliable access to Google Play without juggling multiple client libraries.

## Why curl_cffi?

- **Browser impersonation** – Presents Chrome-like fingerprints to reduce blocking.
- **Modern TLS stack** – Negotiates the same ciphers and extensions as current browsers.
- **Session reuse** – Shares cookies and connection pooling across requests.

## Usage

```python
from gplay_scraper import GPlayScraper

# curl_cffi is configured automatically; no override parameter is required
scraper = GPlayScraper()
```

## Installation

`curl_cffi` is a core dependency and is installed automatically:

```bash
pip install gplay-scraper
# or: uv pip install gplay-scraper
```

## Troubleshooting

- **ImportError for curl_cffi** – Ensure `curl-cffi>=0.5.0` is installed in your environment.
- **Blocked requests** – Keep `curl_cffi` up to date and tune `Config.RATE_LIMIT_DELAY`; the session already impersonates Chrome, so manual user-agent rotation is rarely needed.
- **Custom sessions** – Direct session injection is not supported. The scraper standardises on `curl_cffi` for consistency.
- **No alternate client** – The HTTP backend is fixed to `curl_cffi`; there is no parameter to switch clients.
