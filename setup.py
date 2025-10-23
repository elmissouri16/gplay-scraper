from __future__ import annotations

import pathlib

from setuptools import setup, find_packages

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover - fallback for older pythons
    try:
        import tomli as tomllib  # type: ignore
    except ModuleNotFoundError:  # pragma: no cover - last-resort fallback
        tomllib = None  # type: ignore

ROOT = pathlib.Path(__file__).parent

with (ROOT / "README.md").open("r", encoding="utf-8") as fh:
    long_description = fh.read()

if tomllib is not None:
    with (ROOT / "pyproject.toml").open("rb") as fh:
        project_table = tomllib.load(fh).get("project", {})
    requirements = project_table.get("dependencies", [])
    optional_dependencies = project_table.get("optional-dependencies", {})
else:  # pragma: no cover - minimal fallback if tomllib/tomli unavailable
    requirements = [
        "beautifulsoup4>=4.9.0",
        "curl-cffi>=0.5.0",
    ]
    optional_dependencies = {
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ]
    }

setup(
    name="gplay-scraper",
    version="1.0.4",
    description="🚀 Advanced Google Play Store Scraper - Extract 65+ app fields, reviews, ratings, ASO data, developer info, top charts, search results with a resilient network stack & unlimited pagination support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mohammed Cha",
    author_email="contact@mohammedcha.com",
    maintainer="Mohammed Cha",
    maintainer_email="contact@mohammedcha.com",
    url="https://github.com/mohammedcha/gplay-scraper",
    download_url="https://github.com/mohammedcha/gplay-scraper/archive/v1.0.4.tar.gz",
    project_urls={
        "Homepage": "https://github.com/mohammedcha/gplay-scraper",
        "Documentation": "https://mohammedcha.github.io/gplay-scraper/",
        "Source Code": "https://github.com/mohammedcha/gplay-scraper",
        "Bug Reports": "https://github.com/mohammedcha/gplay-scraper/issues",
        "Feature Requests": "https://github.com/mohammedcha/gplay-scraper/issues",
        "Changelog": "https://github.com/mohammedcha/gplay-scraper/blob/main/CHANGELOG.md",
        "Examples": "https://github.com/mohammedcha/gplay-scraper/tree/main/examples",
        "PyPI": "https://pypi.org/project/gplay-scraper/",
    },
    packages=find_packages(exclude=["tests*", "docs*", "examples*"]),
    install_requires=requirements,
    extras_require=optional_dependencies,
    python_requires=">=3.8",
    keywords="google-play-scraper, playstore-scraper, android-scraper, gplay-scraper, google-play-store, play-store-api, app-data-extraction, app-analytics, mobile-analytics, aso-tools, app-store-optimization, mobile-seo, app-marketing, keyword-research, competitor-analysis, market-research, app-reviews, user-reviews, review-scraper, rating-analysis, sentiment-analysis, developer-tools, api-scraping, web-scraping, data-mining, python-scraper, automation-tools, business-intelligence, market-intelligence, competitive-intelligence, app-monitoring, trend-analysis, performance-tracking, install-tracking, revenue-analysis",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Database",
        "Natural Language :: English",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Typing :: Typed",
    ],
    platforms=["any"],
    include_package_data=True,
    zip_safe=False,
)
