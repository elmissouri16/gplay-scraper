# Contributing to GPlay Scraper

Thank you for your interest in contributing! 

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/gplay-scraper.git`
3. Install dependencies and set up the virtual environment: `uv sync --extra dev`

## Running Tests

```bash
uv run python -m pytest tests/ -v
```

## Code Style

- Follow PEP 8
- Add docstrings to new functions
- Include type hints where appropriate

## Submitting Changes

1. Create a feature branch: `git checkout -b feature-name`
2. Make your changes
3. Add tests for new functionality
4. Run tests to ensure they pass: `uv run python -m pytest tests/ -v`
5. Submit a pull request

## Reporting Issues

Please use GitHub Issues to report bugs or request features.
