"""Method classes for all 7 scraping types.

This module contains 7 method classes. Most provide helper methods to analyze
data, retrieve specific fields, and print selected values; suggest methods also
offer utilities for nested suggestions.
"""

from typing import Any, List, Dict
import logging
from .gplay_scraper import AppScraper, SearchScraper, ReviewsScraper, DeveloperScraper, SimilarScraper, ListScraper, SuggestScraper
from .gplay_parser import AppParser, SearchParser, ReviewsParser, DeveloperParser, SimilarParser, ListParser, SuggestParser
from ..config import Config
from ..exceptions import InvalidAppIdError
from ..utils.http_client import ProxyConfig

# Configure logging
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AppMethods:
    """Methods for extracting app details with 65+ fields."""

    def __init__(self, proxies: ProxyConfig = None):
        """Initialize AppMethods with scraper and parser."""
        self.scraper = AppScraper(proxies=proxies)
        self.parser = AppParser()
    
    def set_proxies(self, proxies: ProxyConfig) -> None:
        """Update proxy configuration for the underlying scraper."""
        self.scraper.set_proxies(proxies)

    def app_analyze(self, app_id: str, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, assets: str = None) -> Dict:
        """Get complete app data with all 65+ fields.
        
        Args:
            app_id: Google Play app ID
            lang: Language code
            country: Country code
            assets: Asset size (SMALL, MEDIUM, LARGE, ORIGINAL)
            
        Returns:
            Dictionary with all app data
            
        Raises:
            InvalidAppIdError: If app_id is invalid
        """
        if not app_id or not isinstance(app_id, str):
            raise InvalidAppIdError(Config.ERROR_MESSAGES["INVALID_APP_ID"])
            
        dataset = self.scraper.scrape_play_store_data(app_id, lang, country)
        app_details = self.parser.parse_app_data(dataset, app_id, self.scraper, assets)
        return self.parser.format_app_data(app_details)

    def app_get_field(self, app_id: str, field: str, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, assets: str = None) -> Any:
        """Get single field value from app data.
        
        Args:
            app_id: Google Play app ID
            field: Field name to retrieve
            lang: Language code
            country: Country code
            assets: Asset size (SMALL, MEDIUM, LARGE, ORIGINAL)
            
        Returns:
            Value of the requested field
        """
        return self.app_analyze(app_id, lang, country, assets).get(field)

    def app_get_fields(self, app_id: str, fields: List[str], lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, assets: str = None) -> Dict[str, Any]:
        """Get multiple field values from app data.
        
        Args:
            app_id: Google Play app ID
            fields: List of field names to retrieve
            lang: Language code
            country: Country code
            assets: Asset size (SMALL, MEDIUM, LARGE, ORIGINAL)
            
        Returns:
            Dictionary with requested fields and values
        """
        data = self.app_analyze(app_id, lang, country, assets)
        return {field: data.get(field) for field in fields}

class SearchMethods:
    """Methods for searching apps by keyword."""

    def __init__(self, proxies: ProxyConfig = None):
        """Initialize SearchMethods with scraper and parser."""
        self.scraper = SearchScraper(proxies=proxies)
        self.parser = SearchParser()
    
    def set_proxies(self, proxies: ProxyConfig) -> None:
        """Update proxy configuration for the underlying scraper."""
        self.scraper.set_proxies(proxies)

    def search_analyze(self, query: str, count: int = Config.DEFAULT_SEARCH_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Dict]:
        """Search for apps and get complete results with pagination support.
        
        Args:
            query: Search query string
            count: Number of results to return
            lang: Language code
            country: Country code
            
        Returns:
            List of dictionaries containing app data
            
        Raises:
            InvalidAppIdError: If query is invalid
        """
        if not query or not isinstance(query, str):
            raise InvalidAppIdError(Config.ERROR_MESSAGES["INVALID_QUERY"])
        
        # scrape_play_store_data now handles pagination automatically
        dataset = self.scraper.scrape_play_store_data(query, count, lang, country)
        
        raw_results = self.parser.parse_search_results(dataset, count)
        return [self.parser.format_search_result(result) for result in raw_results]

    def search_get_field(self, query: str, field: str, count: int = Config.DEFAULT_SEARCH_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Any]:
        """Get single field from all search results.
        
        Args:
            query: Search query string
            field: Field name to retrieve
            count: Number of results
            lang: Language code
            country: Country code
            
        Returns:
            List of field values from all results
        """
        results = self.search_analyze(query, count, lang, country)
        return [app.get(field) for app in results]

    def search_get_fields(self, query: str, fields: List[str], count: int = Config.DEFAULT_SEARCH_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Dict[str, Any]]:
        """Get multiple fields from all search results.
        
        Args:
            query: Search query string
            fields: List of field names to retrieve
            count: Number of results
            lang: Language code
            country: Country code
            
        Returns:
            List of dictionaries with requested fields
        """
        results = self.search_analyze(query, count, lang, country)
        return [{field: app.get(field) for field in fields} for app in results]

class ReviewsMethods:
    """Methods for extracting user reviews and ratings."""

    def __init__(self, proxies: ProxyConfig = None):
        """Initialize ReviewsMethods with scraper and parser."""
        self.scraper = ReviewsScraper(proxies=proxies)
        self.parser = ReviewsParser()
    
    def set_proxies(self, proxies: ProxyConfig) -> None:
        """Update proxy configuration for the underlying scraper."""
        self.scraper.set_proxies(proxies)

    def reviews_analyze(self, app_id: str, count: int = Config.DEFAULT_REVIEWS_COUNT, lang: str = Config.DEFAULT_LANGUAGE, 
                       country: str = Config.DEFAULT_COUNTRY, sort: str = Config.DEFAULT_REVIEWS_SORT) -> List[Dict]:
        """Get user reviews for an app.
        
        Args:
            app_id: Google Play app ID
            count: Number of reviews to fetch
            lang: Language code
            country: Country code
            sort: Sort order (NEWEST, RELEVANT, RATING)
            
        Returns:
            List of review dictionaries
            
        Raises:
            InvalidAppIdError: If app_id is invalid
        """
        if not app_id or not isinstance(app_id, str):
            raise InvalidAppIdError(Config.ERROR_MESSAGES["INVALID_APP_ID"])
            
        if count <= 0:
            return []
            
        try:
            dataset = self.scraper.scrape_reviews_data(app_id, count, lang, country, sort)
            reviews_data = self.parser.parse_multiple_responses(dataset)
        except Exception as e:
            logger.error(Config.ERROR_MESSAGES["REVIEWS_SCRAPE_FAILED"].format(app_id=app_id, error=e))
            raise

        return self.parser.format_reviews_data(reviews_data)

    def reviews_get_field(self, app_id: str, field: str, count: int = Config.DEFAULT_REVIEWS_COUNT, 
                         lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, sort: str = Config.DEFAULT_REVIEWS_SORT) -> List[Any]:
        """Get single field from all reviews.
        
        Args:
            app_id: Google Play app ID
            field: Field name to retrieve
            count: Number of reviews
            lang: Language code
            country: Country code
            sort: Sort order
            
        Returns:
            List of field values from all reviews
        """
        reviews_data = self.reviews_analyze(app_id, count, lang, country, sort)
        return [review.get(field) for review in reviews_data]

    def reviews_get_fields(self, app_id: str, fields: List[str], count: int = Config.DEFAULT_REVIEWS_COUNT,
                          lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, sort: str = Config.DEFAULT_REVIEWS_SORT) -> List[Dict[str, Any]]:
        """Get multiple fields from all reviews.
        
        Args:
            app_id: Google Play app ID
            fields: List of field names to retrieve
            count: Number of reviews
            lang: Language code
            country: Country code
            sort: Sort order
            
        Returns:
            List of dictionaries with requested fields
        """
        reviews_data = self.reviews_analyze(app_id, count, lang, country, sort)
        return [{field: review.get(field) for field in fields} for review in reviews_data]

class DeveloperMethods:
    """Methods for getting all apps from a developer."""

    def __init__(self, proxies: ProxyConfig = None):
        """Initialize DeveloperMethods with scraper and parser."""
        self.scraper = DeveloperScraper(proxies=proxies)
        self.parser = DeveloperParser()
    
    def set_proxies(self, proxies: ProxyConfig) -> None:
        """Update proxy configuration for the underlying scraper."""
        self.scraper.set_proxies(proxies)

    def developer_analyze(self, dev_id: str, count: int = Config.DEFAULT_DEVELOPER_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Dict]:
        """Get all apps from a developer.
        
        Args:
            dev_id: Developer ID (numeric or string)
            count: Number of apps to return
            lang: Language code
            country: Country code
            
        Returns:
            List of app dictionaries
            
        Raises:
            InvalidAppIdError: If dev_id is invalid
        """
        if not dev_id or not isinstance(dev_id, str):
            raise InvalidAppIdError(Config.ERROR_MESSAGES["INVALID_DEV_ID"])
            
        dataset = self.scraper.scrape_play_store_data(dev_id, lang, country)
        apps_data = self.parser.parse_developer_data(dataset, dev_id)
        return self.parser.format_developer_data(apps_data)[:count]

    def developer_get_field(self, dev_id: str, field: str, count: int = Config.DEFAULT_DEVELOPER_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Any]:
        """Get single field from all developer apps.
        
        Args:
            dev_id: Developer ID
            field: Field name to retrieve
            count: Number of apps
            lang: Language code
            country: Country code
            
        Returns:
            List of field values from all apps
        """
        results = self.developer_analyze(dev_id, count, lang, country)
        return [app.get(field) for app in results]

    def developer_get_fields(self, dev_id: str, fields: List[str], count: int = Config.DEFAULT_DEVELOPER_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Dict[str, Any]]:
        """Get multiple fields from all developer apps.
        
        Args:
            dev_id: Developer ID
            fields: List of field names to retrieve
            count: Number of apps
            lang: Language code
            country: Country code
            
        Returns:
            List of dictionaries with requested fields
        """
        results = self.developer_analyze(dev_id, count, lang, country)
        return [{field: app.get(field) for field in fields} for app in results]

class SimilarMethods:
    """Methods for finding similar/competitor apps."""

    def __init__(self, proxies: ProxyConfig = None):
        """Initialize SimilarMethods with scraper and parser."""
        self.scraper = SimilarScraper(proxies=proxies)
        self.parser = SimilarParser()
    
    def set_proxies(self, proxies: ProxyConfig) -> None:
        """Update proxy configuration for the underlying scraper."""
        self.scraper.set_proxies(proxies)

    def similar_analyze(self, app_id: str, count: int = Config.DEFAULT_SIMILAR_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Dict]:
        """Get similar/competitor apps.
        
        Args:
            app_id: Google Play app ID
            count: Number of similar apps to return
            lang: Language code
            country: Country code
            
        Returns:
            List of similar app dictionaries
            
        Raises:
            InvalidAppIdError: If app_id is invalid
        """
        if not app_id or not isinstance(app_id, str):
            raise InvalidAppIdError(Config.ERROR_MESSAGES["INVALID_APP_ID"])
            
        dataset = self.scraper.scrape_play_store_data(app_id, lang, country)
        apps_data = self.parser.parse_similar_data(dataset)
        return self.parser.format_similar_data(apps_data)[:count]

    def similar_get_field(self, app_id: str, field: str, count: int = Config.DEFAULT_SIMILAR_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Any]:
        """Get single field from all similar apps.
        
        Args:
            app_id: Google Play app ID
            field: Field name to retrieve
            count: Number of similar apps
            lang: Language code
            country: Country code
            
        Returns:
            List of field values from all similar apps
        """
        results = self.similar_analyze(app_id, count, lang, country)
        return [app.get(field) for app in results]

    def similar_get_fields(self, app_id: str, fields: List[str], count: int = Config.DEFAULT_SIMILAR_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Dict[str, Any]]:
        """Get multiple fields from all similar apps.
        
        Args:
            app_id: Google Play app ID
            fields: List of field names to retrieve
            count: Number of similar apps
            lang: Language code
            country: Country code
            
        Returns:
            List of dictionaries with requested fields
        """
        results = self.similar_analyze(app_id, count, lang, country)
        return [{field: app.get(field) for field in fields} for app in results]

class ListMethods:
    """Methods for getting top charts (free, paid, grossing)."""

    def __init__(self, proxies: ProxyConfig = None):
        """Initialize ListMethods with scraper and parser."""
        self.scraper = ListScraper(proxies=proxies)
        self.parser = ListParser()
    
    def set_proxies(self, proxies: ProxyConfig) -> None:
        """Update proxy configuration for the underlying scraper."""
        self.scraper.set_proxies(proxies)

    def list_analyze(self, collection: str = Config.DEFAULT_LIST_COLLECTION, category: str = Config.DEFAULT_LIST_CATEGORY, count: int = Config.DEFAULT_LIST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Dict]:
        """Get top charts (top free, top paid, top grossing).
        
        Args:
            collection: Collection type (TOP_FREE, TOP_PAID, TOP_GROSSING)
            category: App category
            count: Number of apps to return
            lang: Language code
            country: Country code
            
        Returns:
            List of app dictionaries from top charts
        """
        dataset = self.scraper.scrape_play_store_data(collection, category, count, lang, country)
        apps_data = self.parser.parse_list_data(dataset, count)
        return self.parser.format_list_data(apps_data)

    def list_get_field(self, collection: str, field: str, category: str = Config.DEFAULT_LIST_CATEGORY, count: int = Config.DEFAULT_LIST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Any]:
        """Get single field from all list apps.
        
        Args:
            collection: Collection type
            field: Field name to retrieve
            category: App category
            count: Number of apps
            lang: Language code
            country: Country code
            
        Returns:
            List of field values from all apps
        """
        results = self.list_analyze(collection, category, count, lang, country)
        return [app.get(field) for app in results]

    def list_get_fields(self, collection: str, fields: List[str], category: str = Config.DEFAULT_LIST_CATEGORY, count: int = Config.DEFAULT_LIST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Dict[str, Any]]:
        """Get multiple fields from all list apps.
        
        Args:
            collection: Collection type
            fields: List of field names to retrieve
            category: App category
            count: Number of apps
            lang: Language code
            country: Country code
            
        Returns:
            List of dictionaries with requested fields
        """
        results = self.list_analyze(collection, category, count, lang, country)
        return [{field: app.get(field) for field in fields} for app in results]

class SuggestMethods:
    """Methods for getting search suggestions and autocomplete."""

    def __init__(self, proxies: ProxyConfig = None):
        """Initialize SuggestMethods with scraper and parser."""
        self.scraper = SuggestScraper(proxies=proxies)
        self.parser = SuggestParser()
    
    def set_proxies(self, proxies: ProxyConfig) -> None:
        """Update proxy configuration for the underlying scraper."""
        self.scraper.set_proxies(proxies)

    def suggest_analyze(self, term: str, count: int = Config.DEFAULT_SUGGEST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[str]:
        """Get search suggestions for a term.
        
        Args:
            term: Search term
            count: Number of suggestions to return
            lang: Language code
            country: Country code
            
        Returns:
            List of suggestion strings
            
        Raises:
            InvalidAppIdError: If term is invalid
        """
        if not term or not isinstance(term, str):
            raise InvalidAppIdError(Config.ERROR_MESSAGES["INVALID_QUERY"])
        
        dataset = self.scraper.scrape_suggestions(term, lang, country)
        suggestions = self.parser.parse_suggestions(dataset)
        return self.parser.format_suggestions(suggestions[:count])

    def suggest_nested(self, term: str, count: int = Config.DEFAULT_SUGGEST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> Dict[str, List[str]]:
        """Get nested suggestions (suggestions for suggestions).
        
        Args:
            term: Search term
            count: Number of suggestions per level
            lang: Language code
            country: Country code
            
        Returns:
            Dictionary mapping suggestions to their nested suggestions
            
        Raises:
            InvalidAppIdError: If term is invalid
        """
        if not term or not isinstance(term, str):
            raise InvalidAppIdError(Config.ERROR_MESSAGES["INVALID_QUERY"])
        
        first_level = self.suggest_analyze(term, count, lang, country)
        results = {}
        for suggestion in first_level:
            second_level = self.suggest_analyze(suggestion, count, lang, country)
            results[suggestion] = second_level
        return results
