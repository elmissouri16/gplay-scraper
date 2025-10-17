# Contributing

Thank you for investing time in GPlay Scraper! The canonical contributor guide lives at [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## Quick Start

```bash
git clone https://github.com/yourusername/gplay-scraper.git
cd gplay-scraper
pip install -e .
pip install -r requirements.txt  # optional tooling
```

Run the test suite before opening a pull request:

```bash
python -m pytest tests -v
```

## Coding Guidelines

- Follow PEP 8 with four-space indentation and informative naming.
- Add type hints and concise docstrings on new or updated APIs.
- Keep commits focused with imperative messages (for example, `Fix pagination delay`).

## Documentation

- Update Markdown files under `docs/` or `README/` when you change behaviour or defaults.
- Regenerate examples if your changes modify output snippets.

## Submitting Changes

1. Create a feature branch.
2. Make changes and add or update tests.
3. Run `python -m pytest tests -v`.
4. Open a pull request that describes motivation, key changes, and verification steps.
