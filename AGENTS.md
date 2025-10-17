# Repository Guidelines

## Project Structure & Module Organization
Core scraping logic lives in `gplay_scraper/`, with HTTP clients and dispatching under `core/`, reusable dataclasses in `models/`, shared helpers in `utils/`, and API entry points in `app.py` and `__init__.py`. Tests mirror those areas in `tests/` (`test_app_methods.py`, `test_search_methods.py`, etc.) to cover each public method type. Markdown docs live in `docs/`, runnable examples in `examples/`, static assets in `assets/`, and sample JSON payloads in `output/`. Dependency pins are maintained in `pyproject.toml` and `requirements.txt`.

## Build, Test, and Development Commands
- `pip install -e .` — install the library in editable mode for local iteration.
- `pip install -r requirements.txt` — pull optional clients and tooling used in CI.
- `python -m pytest tests -v` — execute the full test suite with verbose output.

## Coding Style & Naming Conventions
Follow PEP 8 defaults with four-space indentation and descriptive `snake_case` for routines; module-level constants stay upper snake case. Prefer type hints on new or touched signatures and include concise docstrings when you add behavior. Classes should use `PascalCase`, pytest fixtures remain lowercase, and HTTP client identifiers should track the existing `GPlayScraper` public surface.

## Testing Guidelines
Use pytest for new coverage and place files alongside the feature you extend (e.g., `tests/test_reviews_methods.py`). Name tests `test_<behavior>` and group related assertions inside descriptive classes or functions. When adding network-sensitive logic, rely on fixtures or recorded responses to keep the suite deterministic. Run `python -m pytest tests -k your_scope -vv` while iterating, then confirm `python -m pytest tests -v` before opening a pull request.

## Commit & Pull Request Guidelines
Commits in this repository favor short, Title Case messages (`Release v1.0.4: Add assets parameter`) and occasionally prefix emoji for clarity; follow that pattern with an imperative summary and optional scope. Push feature work on topic branches, reference any GitHub issues in the body, and include before/after notes for CLI-facing changes. Pull requests should describe motivation, list verification steps, attach relevant screenshots or JSON snippets, and confirm pytest results in the checklist.

## Documentation & Examples
Update user-facing docs when signatures or defaults change by editing the Markdown pages under `docs/` or the method guides in `README/`. Keep example scripts in `examples/` minimal and runnable with the documented commands, noting any required environment variables or proxy configuration in docstrings or README snippets.
