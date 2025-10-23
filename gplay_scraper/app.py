"""Main GPlayScraper class that provides unified access to all scraping methods.

This module contains the main GPlayScraper class which aggregates all 7 method types
and provides a comprehensive set of functions for interacting with Google Play Store data.
"""

from .core.gplay_methods import AppMethods, SearchMethods, ReviewsMethods, DeveloperMethods, SimilarMethods, ListMethods, SuggestMethods
from .config import Config
from .utils.http_client import ProxyConfig
from typing import Any, List, Dict


class GPlayScraper:
    """Main scraper class providing access to all Google Play Store scraping methods.
    
    This class aggregates 7 method types:
    - App Methods: Extract 65+ fields from any app
    - Search Methods: Search for apps by keyword
    - Reviews Methods: Extract user reviews and ratings
    - Developer Methods: Get all apps from a developer
    - List Methods: Get top charts (free, paid, grossing)
    - Similar Methods: Find similar/competitor apps
    - Suggest Methods: Get search suggestions
    
    Args:
        proxies: Optional proxy configuration applied to all HTTP calls.
            Accepts either a string (`"http://host:port"`) which is applied to
            both HTTP and HTTPS requests, or a mapping such as
            `{"http": "http://proxy", "https": "http://proxy2"}`.
    """
    
    def __init__(self, proxies: ProxyConfig = None):
        """Initialize GPlayScraper with all method types.
        
        Args:
            proxies: Optional proxy configuration applied to all HTTP calls.
        """
        # Initialize all 7 method types
        self.app_methods = AppMethods(proxies=proxies)
        self.search_methods = SearchMethods(proxies=proxies)
        self.reviews_methods = ReviewsMethods(proxies=proxies)
        self.developer_methods = DeveloperMethods(proxies=proxies)
        self.similar_methods = SimilarMethods(proxies=proxies)
        self.list_methods = ListMethods(proxies=proxies)
        self.suggest_methods = SuggestMethods(proxies=proxies)

    def set_proxies(self, proxies: ProxyConfig) -> None:
        """Update proxy configuration for all method groups at runtime.

        Args:
            proxies: Either a proxy URL string or a mapping of scheme to proxy URL.
                Passing ``None`` clears any existing proxy configuration.
        """
        self.app_methods.set_proxies(proxies)
        self.search_methods.set_proxies(proxies)
        self.reviews_methods.set_proxies(proxies)
        self.developer_methods.set_proxies(proxies)
        self.similar_methods.set_proxies(proxies)
        self.list_methods.set_proxies(proxies)
        self.suggest_methods.set_proxies(proxies)

    # ==================== App Methods ====================
    
    def app_analyze(self, app_id: str, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, assets: str = None) -> Dict:
        """Get complete app data with 65+ fields.
        
        Args:
            app_id: Google Play app ID (e.g., 'com.whatsapp')
            lang: Language code (default: 'en')
            country: Country code (default: 'us')
            assets: Asset size (SMALL=512px, MEDIUM=1024px, LARGE=2048px, ORIGINAL=max)
            
        Returns:
            Dictionary containing all app data
        """
        return self.app_methods.app_analyze(app_id, lang, country, assets)

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
        return self.app_methods.app_get_field(app_id, field, lang, country, assets)

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
        return self.app_methods.app_get_fields(app_id, fields, lang, country, assets)

    def app_print_field(self, app_id: str, field: str, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, assets: str = None) -> None:
        """Print single field value to console.
        
        Args:
            app_id: Google Play app ID
            field: Field name to print
            lang: Language code
            country: Country code
            assets: Asset size (SMALL, MEDIUM, LARGE, ORIGINAL)
        """
        return self.app_methods.app_print_field(app_id, field, lang, country, assets)

    def app_print_fields(self, app_id: str, fields: List[str], lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, assets: str = None) -> None:
        """Print multiple field values to console.
        
        Args:
            app_id: Google Play app ID
            fields: List of field names to print
            lang: Language code
            country: Country code
            assets: Asset size (SMALL, MEDIUM, LARGE, ORIGINAL)
        """
        return self.app_methods.app_print_fields(app_id, fields, lang, country, assets)

    # ==================== Search Methods ====================
    
    def search_analyze(self, query: str, count: int = Config.DEFAULT_SEARCH_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Dict]:
        """Search for apps and get complete results.
        
        Args:
            query: Search query string
            count: Number of results to return
            lang: Language code
            country: Country code
            
        Returns:
            List of dictionaries containing app data
        """
        return self.search_methods.search_analyze(query, count, lang, country)

    def search_get_field(self, query: str, field: str, count: int = Config.DEFAULT_SEARCH_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Any]:
        """Get single field from search results.
        
        Args:
            query: Search query string
            field: Field name to retrieve
            count: Number of results
            lang: Language code
            country: Country code
            
        Returns:
            List of field values
        """
        return self.search_methods.search_get_field(query, field, count, lang, country)

    def search_get_fields(self, query: str, fields: List[str], count: int = Config.DEFAULT_SEARCH_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Dict[str, Any]]:
        """Get multiple fields from search results.
        
        Args:
            query: Search query string
            fields: List of field names
            count: Number of results
            lang: Language code
            country: Country code
            
        Returns:
            List of dictionaries with requested fields
        """
        return self.search_methods.search_get_fields(query, fields, count, lang, country)

    def search_print_field(self, query: str, field: str, count: int = Config.DEFAULT_SEARCH_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print single field from search results.
        
        Args:
            query: Search query string
            field: Field name to print
            count: Number of results
            lang: Language code
            country: Country code
        """
        return self.search_methods.search_print_field(query, field, count, lang, country)

    def search_print_fields(self, query: str, fields: List[str], count: int = Config.DEFAULT_SEARCH_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print multiple fields from search results.
        
        Args:
            query: Search query string
            fields: List of field names
            count: Number of results
            lang: Language code
            country: Country code
        """
        return self.search_methods.search_print_fields(query, fields, count, lang, country)

    # ==================== Reviews Methods ====================
    
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
        """
        return self.reviews_methods.reviews_analyze(app_id, count, lang, country, sort)

    def reviews_get_field(self, app_id: str, field: str, count: int = Config.DEFAULT_REVIEWS_COUNT, 
                         lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, sort: str = Config.DEFAULT_REVIEWS_SORT) -> List[Any]:
        """Get single field from reviews.
        
        Args:
            app_id: Google Play app ID
            field: Field name to retrieve
            count: Number of reviews
            lang: Language code
            country: Country code
            sort: Sort order
            
        Returns:
            List of field values
        """
        return self.reviews_methods.reviews_get_field(app_id, field, count, lang, country, sort)

    def reviews_get_fields(self, app_id: str, fields: List[str], count: int = Config.DEFAULT_REVIEWS_COUNT,
                          lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, sort: str = Config.DEFAULT_REVIEWS_SORT) -> List[Dict[str, Any]]:
        """Get multiple fields from reviews.
        
        Args:
            app_id: Google Play app ID
            fields: List of field names
            count: Number of reviews
            lang: Language code
            country: Country code
            sort: Sort order
            
        Returns:
            List of dictionaries with requested fields
        """
        return self.reviews_methods.reviews_get_fields(app_id, fields, count, lang, country, sort)

    def reviews_print_field(self, app_id: str, field: str, count: int = Config.DEFAULT_REVIEWS_COUNT,
                           lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, sort: str = Config.DEFAULT_REVIEWS_SORT) -> None:
        """Print single field from reviews.
        
        Args:
            app_id: Google Play app ID
            field: Field name to print
            count: Number of reviews
            lang: Language code
            country: Country code
            sort: Sort order
        """
        return self.reviews_methods.reviews_print_field(app_id, field, count, lang, country, sort)

    def reviews_print_fields(self, app_id: str, fields: List[str], count: int = Config.DEFAULT_REVIEWS_COUNT,
                            lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, sort: str = Config.DEFAULT_REVIEWS_SORT) -> None:
        """Print multiple fields from reviews.
        
        Args:
            app_id: Google Play app ID
            fields: List of field names
            count: Number of reviews
            lang: Language code
            country: Country code
            sort: Sort order
        """
        return self.reviews_methods.reviews_print_fields(app_id, fields, count, lang, country, sort)

    # ==================== Developer Methods ====================
    
    def developer_analyze(self, dev_id: str, count: int = Config.DEFAULT_DEVELOPER_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Dict]:
        """Get all apps from a developer.
        
        Args:
            dev_id: Developer ID (numeric or string)
            count: Number of apps to return
            lang: Language code
            country: Country code
            
        Returns:
            List of app dictionaries
        """
        return self.developer_methods.developer_analyze(dev_id, count, lang, country)

    def developer_get_field(self, dev_id: str, field: str, count: int = Config.DEFAULT_DEVELOPER_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Any]:
        """Get single field from developer apps.
        
        Args:
            dev_id: Developer ID
            field: Field name to retrieve
            count: Number of apps
            lang: Language code
            country: Country code
            
        Returns:
            List of field values
        """
        return self.developer_methods.developer_get_field(dev_id, field, count, lang, country)

    def developer_get_fields(self, dev_id: str, fields: List[str], count: int = Config.DEFAULT_DEVELOPER_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Dict[str, Any]]:
        """Get multiple fields from developer apps.
        
        Args:
            dev_id: Developer ID
            fields: List of field names
            count: Number of apps
            lang: Language code
            country: Country code
            
        Returns:
            List of dictionaries with requested fields
        """
        return self.developer_methods.developer_get_fields(dev_id, fields, count, lang, country)

    def developer_print_field(self, dev_id: str, field: str, count: int = Config.DEFAULT_DEVELOPER_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print single field from developer apps.
        
        Args:
            dev_id: Developer ID
            field: Field name to print
            count: Number of apps
            lang: Language code
            country: Country code
        """
        return self.developer_methods.developer_print_field(dev_id, field, count, lang, country)

    def developer_print_fields(self, dev_id: str, fields: List[str], count: int = Config.DEFAULT_DEVELOPER_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print multiple fields from developer apps.
        
        Args:
            dev_id: Developer ID
            fields: List of field names
            count: Number of apps
            lang: Language code
            country: Country code
        """
        return self.developer_methods.developer_print_fields(dev_id, fields, count, lang, country)

    # ==================== Similar Methods ====================
    
    def similar_analyze(self, app_id: str, count: int = Config.DEFAULT_SIMILAR_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Dict]:
        """Get similar/competitor apps.
        
        Args:
            app_id: Google Play app ID
            count: Number of similar apps to return
            lang: Language code
            country: Country code
            
        Returns:
            List of similar app dictionaries
        """
        return self.similar_methods.similar_analyze(app_id, count, lang, country)

    def similar_get_field(self, app_id: str, field: str, count: int = Config.DEFAULT_SIMILAR_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Any]:
        """Get single field from similar apps.
        
        Args:
            app_id: Google Play app ID
            field: Field name to retrieve
            count: Number of similar apps
            lang: Language code
            country: Country code
            
        Returns:
            List of field values
        """
        return self.similar_methods.similar_get_field(app_id, field, count, lang, country)

    def similar_get_fields(self, app_id: str, fields: List[str], count: int = Config.DEFAULT_SIMILAR_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Dict[str, Any]]:
        """Get multiple fields from similar apps.
        
        Args:
            app_id: Google Play app ID
            fields: List of field names
            count: Number of similar apps
            lang: Language code
            country: Country code
            
        Returns:
            List of dictionaries with requested fields
        """
        return self.similar_methods.similar_get_fields(app_id, fields, count, lang, country)

    def similar_print_field(self, app_id: str, field: str, count: int = Config.DEFAULT_SIMILAR_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print single field from similar apps.
        
        Args:
            app_id: Google Play app ID
            field: Field name to print
            count: Number of similar apps
            lang: Language code
            country: Country code
        """
        return self.similar_methods.similar_print_field(app_id, field, count, lang, country)

    def similar_print_fields(self, app_id: str, fields: List[str], count: int = Config.DEFAULT_SIMILAR_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print multiple fields from similar apps.
        
        Args:
            app_id: Google Play app ID
            fields: List of field names
            count: Number of similar apps
            lang: Language code
            country: Country code
        """
        return self.similar_methods.similar_print_fields(app_id, fields, count, lang, country)

    # ==================== List Methods ====================
    
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
        return self.list_methods.list_analyze(collection, category, count, lang, country)

    def list_get_field(self, collection: str, field: str, category: str = Config.DEFAULT_LIST_CATEGORY, count: int = Config.DEFAULT_LIST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Any]:
        """Get single field from top charts.
        
        Args:
            collection: Collection type
            field: Field name to retrieve
            category: App category
            count: Number of apps
            lang: Language code
            country: Country code
            
        Returns:
            List of field values
        """
        return self.list_methods.list_get_field(collection, field, category, count, lang, country)

    def list_get_fields(self, collection: str, fields: List[str], category: str = Config.DEFAULT_LIST_CATEGORY, count: int = Config.DEFAULT_LIST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[Dict[str, Any]]:
        """Get multiple fields from top charts.
        
        Args:
            collection: Collection type
            fields: List of field names
            category: App category
            count: Number of apps
            lang: Language code
            country: Country code
            
        Returns:
            List of dictionaries with requested fields
        """
        return self.list_methods.list_get_fields(collection, fields, category, count, lang, country)

    def list_print_field(self, collection: str, field: str, category: str = Config.DEFAULT_LIST_CATEGORY, count: int = Config.DEFAULT_LIST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print single field from top charts.
        
        Args:
            collection: Collection type
            field: Field name to print
            category: App category
            count: Number of apps
            lang: Language code
            country: Country code
        """
        return self.list_methods.list_print_field(collection, field, category, count, lang, country)

    def list_print_fields(self, collection: str, fields: List[str], category: str = Config.DEFAULT_LIST_CATEGORY, count: int = Config.DEFAULT_LIST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print multiple fields from top charts.
        
        Args:
            collection: Collection type
            fields: List of field names
            category: App category
            count: Number of apps
            lang: Language code
            country: Country code
        """
        return self.list_methods.list_print_fields(collection, fields, category, count, lang, country)

    # ==================== Suggest Methods ====================
    
    def suggest_analyze(self, term: str, count: int = Config.DEFAULT_SUGGEST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> List[str]:
        """Get search suggestions for a term.
        
        Args:
            term: Search term
            count: Number of suggestions to return
            lang: Language code
            country: Country code
            
        Returns:
            List of suggestion strings
        """
        return self.suggest_methods.suggest_analyze(term, count, lang, country)

    def suggest_nested(self, term: str, count: int = Config.DEFAULT_SUGGEST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> Dict[str, List[str]]:
        """Get nested suggestions (suggestions for suggestions).
        
        Args:
            term: Search term
            count: Number of suggestions
            lang: Language code
            country: Country code
            
        Returns:
            Dictionary mapping terms to their suggestions
        """
        return self.suggest_methods.suggest_nested(term, count, lang, country)

    def suggest_print_nested(self, term: str, count: int = Config.DEFAULT_SUGGEST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print nested suggestions as JSON.
        
        Args:
            term: Search term
            count: Number of suggestions
            lang: Language code
            country: Country code
        """
        return self.suggest_methods.suggest_print_nested(term, count, lang, country)
