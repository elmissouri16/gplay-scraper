# Repository Guidelines

## Project Structure & Module Organization
- `gplay_scraper/` holds the scraping engine: request orchestration in `core/`, data models in `models/`, and helpers in `utils/`.
- Public entry points live in `gplay_scraper/__init__.py` and `gplay_scraper/app.py`.
- Tests mirror the package under `tests/` (for example `tests/test_app_methods.py`), while runnable demos stay in `examples/`.
- Markdown docs sit in `docs/`, static assets in `assets/`, and sample responses in `output/`. Dependency pins reside in `pyproject.toml` and `uv.lock`.

## Build, Test, and Development Commands
- `uv sync --extra dev` — create `.venv/` and install project plus developer dependencies in editable mode.
- `uv run python -m pytest tests -v` — execute the full test suite; add `-k pattern` to focus on a feature.
- `uv run python -m pytest tests -k developer -vv` — iterate quickly on focused scenarios.
- Docs require no build step—edit `docs/*.md` directly and preview with your editor or GitHub.

## Coding Style & Naming Conventions
- Adhere to PEP 8 with four-space indentation, `snake_case` for functions/modules, `PascalCase` for classes, and UPPER_SNAKE_CASE for constants.
- Add type hints and concise docstrings when touching signatures; keep public APIs descriptive.
- Prefer explicit helpers over magic values, and keep logging consistent with existing modules.
- Use comments sparingly to clarify non-obvious behaviour rather than restating code.

## Testing Guidelines
- Use `pytest` exclusively; place new coverage alongside related modules within `tests/`.
- Name tests `test_<behavior>` and group related assertions in helper functions or classes.
- Mock or fixture external calls to keep runs deterministic; avoid live network traffic in CI.
- Ensure `uv run python -m pytest tests -v` passes before submitting and note any expected skips in the PR body.

## Commit & Pull Request Guidelines
- Commits favour short, Title Case messages (optional emoji prefix), e.g., `🚀 Improve Review Parsing`.
- Limit each commit to a logical change set and reference GitHub issues where applicable.
- Pull requests should outline motivation, list verification commands, link supporting issues, and attach screenshots or JSON diffs for user-facing changes.
- State test outcomes explicitly and mention follow-up tasks or known limitations.

## Configuration & Operational Tips
- `curl_cffi` is the sole supported HTTP backend; do not introduce alternative clients without discussion.
- Honour `Config.RATE_LIMIT_DELAY` and other defaults when extending features, exposing overrides through `Config` utilities or documented environment variables (`GPLAY_TIMEOUT`, `GPLAY_RATE_LIMIT`).
- Keep secrets and proxies out of the repository; document required environment variables in examples instead.
