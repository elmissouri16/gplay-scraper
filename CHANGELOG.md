# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Breaking Changes

- Simplified network configuration; the scraper now relies on an internal session with no external backend hooks.
- Dropped the `http_client` initializer argument; networking is fully managed by the scraper.

### Dependency Updates

- Dropped `requests`, `httpx`, `tls-client`, `urllib3`, `cloudscraper`, and `aiohttp` from core requirements.

### Documentation

- Retired the Sphinx toolchain in favour of Markdown docs that live directly under `docs/`.
- Updated contributor workflows to recommend `uv` for local development while keeping pip the default for end users.
- Documented the dual pip/uv installation paths and clarified how to install development extras.

## [1.0.4] - 2025-10-16

### New Features

- **Assets Parameter**: Added configurable image sizes for all app methods
  - `SMALL` (512px width)
  - `MEDIUM` (1024px width) - Default
  - `LARGE` (2048px width)
  - `ORIGINAL` (Maximum size)
  - Available in all app methods: `app_analyze()`, `app_get_field()`, `app_get_fields()`
  - Affects icon, headerImage, screenshots, and videoImage URLs

### Bug Fixes

- **Release Date Fallback**: Fixed missing release dates when using language/country parameters
  - Added automatic fallback request without `hl`/`gl` parameters when release date is null
  - Ensures release date extraction for apps in all regions
- **Path Resolution**: Fixed various path-related issues in data extraction
- **Image URL Processing**: Improved image URL formatting with proper size parameters

### Usage Examples

```python
# Use different asset sizes
data = scraper.app_analyze("com.whatsapp", assets="LARGE")
icon = scraper.app_get_field("com.whatsapp", "icon", assets="SMALL")
summary = scraper.app_get_fields("com.whatsapp", ["title", "score"], assets="ORIGINAL")
print(summary)
```

## [1.0.3] - 2025-10-15

### New Features

- **Enhanced Search Pagination**: Now able to fetch unlimited search results (300+) with automatic pagination, not limited to 50 results anymore
- **Improved Search Performance**: Optimized search result fetching with better token handling and batch processing

### Bug Fixes & Code Quality Improvements

- **Code Review**: Addressed security vulnerabilities and code quality issues
- **Error Handling**: Improved error handling patterns across all modules
- **Performance**: Optimized JSON parsing and network fallback logic
- **Security**: Fixed potential SSRF and injection vulnerabilities
- **Maintainability**: Enhanced code readability and documentation

## [1.0.2] - 2025-01-15

### Major Release - Complete Library Redesign 🚀

This version represents a complete rewrite of GPlay Scraper with a focus on modularity, extensibility, and comprehensive data extraction across all Google Play Store features.

### New Features

#### 7 Method Types with 42 Functions

- **App Methods** - Extract 65+ data fields from any app (ratings, installs, pricing, permissions, screenshots, etc.)
- **Search Methods** - Search Google Play Store apps with comprehensive filtering and pagination
- **Reviews Methods** - Extract user reviews with ratings, timestamps, helpful votes, and detailed feedback
- **Developer Methods** - Get all apps published by a specific developer using developer ID
- **List Methods** - Access top charts (TOP_FREE, TOP_PAID, TOP_GROSSING) by category with 54 categories
- **Similar Methods** - Find similar/competitor apps for market research and competitive analysis
- **Suggest Methods** - Get search suggestions and autocomplete for ASO keyword research

Each method type includes convenience helpers:
- `analyze()` - Get all data as dictionary/list
- `get_field()` - Get single field value
- `get_fields()` - Get multiple fields as dictionary
- Suggest methods additionally provide `nested()` for recursive suggestions

#### Multi-Language & Multi-Region Support

- Support for 100+ languages (en, es, fr, de, ja, ko, zh, ar, etc.)
- Support for 150+ countries (us, gb, ca, au, in, br, jp, etc.)
- Get localized app data, reviews, and search results
- Region-specific pricing and availability information

#### Comprehensive Data Extraction

- **65+ App Fields**: title, developer, ratings, installs, price, screenshots, permissions, release date, update date, size, version, content rating, privacy policy, and more
- **Review Data**: user name, rating, review text, timestamp, app version, helpful votes, developer reply
- **Search Results**: app ID, title, developer, rating, price, icon, screenshots, description snippet
- **Developer Portfolio**: all apps from a developer with complete metadata
- **Top Charts**: ranked lists with install counts, ratings, and trending data
- **Similar Apps**: competitor analysis with relevance scoring
- **Search Suggestions**: popular keywords and autocomplete terms

#### Enhanced Architecture

- **Modular Design**: Separate classes for methods, scrapers, and parsers
- **Core Modules**: `gplay_methods.py`, `gplay_scraper.py`, `gplay_parser.py`
- **Session Abstraction**: Dedicated class providing pluggable request handling
- **Element Specs**: Reusable CSS selector specifications for data extraction
- **Helper Utilities**: Text processing, date parsing, JSON cleaning, age calculation
- **Exception Hierarchy**: 6 custom exception types for specific error scenarios

#### Documentation & Testing

- **Comprehensive Docstrings**: All 42 methods, 7 scrapers, 7 parsers, and utility functions documented
- **Sphinx Documentation**: Professional HTML documentation with examples, API reference, and guides
- **Fields Reference**: Complete reference of all 65+ fields, categories, and parameters
- **Unit Tests**: Complete test coverage for all 7 method types
- **Examples**: Real-world usage examples for each method type

#### Configuration & Customization

- **Configurable Parameters**: Language, country, count, sort order, collection type
- **Rate Limiting**: Built-in delays to prevent blocking (configurable)
- **Error Handling**: Graceful fallbacks and informative error messages
- **Logging**: Detailed logging for debugging and monitoring
- **Timeout Control**: Configurable request timeouts
- **Retry Logic**: Automatic retries with exponential backoff

### Breaking Changes

- Complete API redesign - not backward compatible with v1.0.1
- Method names changed from `get_app_details()` to `app_analyze()`
- New parameter structure for all methods
- Exception types renamed and reorganized

### Migration Guide

Old (v1.0.1):
```python
scraper = GPlayScraper()
data = scraper.get_app_details("com.whatsapp")
```

New (v1.0.2):
```python
scraper = GPlayScraper()
data = scraper.app_analyze("com.whatsapp")
```

### Performance Improvements

- Faster JSON parsing with optimized regex patterns
- Reduced memory usage with streaming parsers
- Better caching of internal network sessions
- Parallel request support with async clients

### Bug Fixes

- Fixed JSON parsing for apps with special characters in descriptions
- Fixed review extraction for apps with no reviews
- Fixed developer ID extraction from developer pages
- Fixed category parsing for apps in multiple categories
- Fixed price parsing for apps with regional pricing
- Fixed screenshot URL extraction for apps with video previews

## [1.0.1] - 2025-10-07

### Added
- **Paid App Support**: Fixed JSON parsing issues for paid apps with malformed data structures
- **Reviews Extraction**: Successfully extracts user reviews for both free and paid apps
- **Organized Output**: Restructured JSON output with logical field grouping:
  - Basic Information
  - Category & Genre
  - Release & Updates
  - Media Content
  - Install Statistics
  - Ratings & Reviews
  - Advertising
  - Technical Details
  - Content Rating
  - Privacy & Security
  - Pricing & Monetization
  - Developer Information
  - ASO Analysis
- **Enhanced JSON Parser**: Bracket-matching algorithm for complex nested structures
- **Original Price Field**: Added `originalPrice` field for sale price tracking

### Fixed
- **JSON Parsing Errors**: Resolved "Expecting ',' delimiter" errors for paid apps
- **Reviews Data**: Fixed empty reviews arrays by implementing alternative parsing methods
- **Malformed Data Handling**: Improved handling of unquoted keys and malformed JSON from Play Store

### Improved
- **Error Handling**: Better fallback mechanisms for JSON parsing failures
- **Data Extraction**: More robust extraction for apps with complex pricing structures
- **Code Organization**: Cleaner separation of parsing logic and error recovery

## [1.0.0] - 2025-10-06

### Added
- Initial release of GPlay Scraper
- Complete Google Play Store app data extraction
- ASO (App Store Optimization) analysis
- Modular architecture with separate core modules
- Support for 60+ data fields including:
  - Basic app information
  - Install statistics and metrics
  - Ratings and reviews data
  - Technical specifications
  - Developer information
  - Media content (screenshots, videos, icons)
  - Pricing and monetization details
  - ASO keyword analysis
- Multiple access methods:
  - `analyze()` - Complete app analysis
  - `get_field()` - Single field retrieval
  - `get_fields()` - Multiple field retrieval
- Comprehensive documentation and examples
- Error handling and logging
- Rate limiting considerations
- Cross-platform compatibility

### Features
- Web scraping of Google Play Store pages
- JSON data extraction and parsing
- Automatic install metrics calculation
- Keyword frequency analysis
- Readability scoring
- Review data extraction
- Image URL processing
- Date parsing and age calculation
