"""Custom exceptions for GPlay Scraper.

This module defines all custom exceptions used throughout the library.
"""


class GPlayScraperError(Exception):
    """Base exception for all GPlay Scraper errors."""
    pass


class InvalidAppIdError(GPlayScraperError):
    """Raised when an invalid app ID, dev ID, or query is provided."""
    pass


class AppNotFoundError(GPlayScraperError):
    """Raised when an app, developer, or resource is not found (404 error)."""
    pass


class RateLimitError(GPlayScraperError):
    """Raised when rate limiting is triggered by Google Play Store."""
    pass


class NetworkError(GPlayScraperError):
    """Raised when network requests fail."""
    pass


class DataParsingError(GPlayScraperError):
    """Raised when parsing JSON or HTML data fails."""
    pass