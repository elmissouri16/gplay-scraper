"""Method classes for all 7 scraping types.

This module contains 7 method classes, each providing 6 functions (except Suggest with 4):
- analyze(): Get all data
- get_field(): Get single field
- get_fields(): Get multiple fields
- print_field(): Print single field
- print_fields(): Print multiple fields
- print_all(): Print all data as JSON
"""

import json
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
    def __init__(self, http_client: str = None, proxies: ProxyConfig = None):
        """Initialize AppMethods with scraper and parser.
        
        Args:
            http_client: Optional HTTP client name
            proxies: Optional proxy configuration
        """
        self.scraper = AppScraper(http_client=http_client, proxies=proxies)
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

    def app_print_field(self, app_id: str, field: str, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, assets: str = None) -> None:
        """Print single field value to console.
        
        Args:
            app_id: Google Play app ID
            field: Field name to print
            lang: Language code
            country: Country code
            assets: Asset size (SMALL, MEDIUM, LARGE, ORIGINAL)
        """
        value = self.app_get_field(app_id, field, lang, country, assets)
        try:
            print(f"{field}: {value}")
        except UnicodeEncodeError:
            print(f"{field}: {repr(value)}")

    def app_print_fields(self, app_id: str, fields: List[str], lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, assets: str = None) -> None:
        """Print multiple field values to console.
        
        Args:
            app_id: Google Play app ID
            fields: List of field names to print
            lang: Language code
            country: Country code
            assets: Asset size (SMALL, MEDIUM, LARGE, ORIGINAL)
        """
        data = self.app_get_fields(app_id, fields, lang, country, assets)
        for field, value in data.items():
            try:
                print(f"{field}: {value}")
            except UnicodeEncodeError:
                print(f"{field}: {repr(value)}")

    def app_print_all(self, app_id: str, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, assets: str = None) -> None:
        """Print all app data as JSON to console.
        
        Args:
            app_id: Google Play app ID
            lang: Language code
            country: Country code
            assets: Asset size (SMALL, MEDIUM, LARGE, ORIGINAL)
        """
        data = self.app_analyze(app_id, lang, country, assets)
        try:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except UnicodeEncodeError:
            print(json.dumps(data, indent=2, ensure_ascii=True))


class SearchMethods:
    """Methods for searching apps by keyword."""
    def __init__(self, http_client: str = None, proxies: ProxyConfig = None):
        """Initialize SearchMethods with scraper and parser.
        
        Args:
            http_client: Optional HTTP client name
            proxies: Optional proxy configuration
        """
        self.scraper = SearchScraper(http_client=http_client, proxies=proxies)
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

    def search_print_field(self, query: str, field: str, count: int = Config.DEFAULT_SEARCH_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print single field from all search results.
        
        Args:
            query: Search query string
            field: Field name to print
            count: Number of results
            lang: Language code
            country: Country code
        """
        values = self.search_get_field(query, field, count, lang, country)
        for i, value in enumerate(values):
            try:
                print(f"{i}. {field}: {value}")
            except UnicodeEncodeError:
                print(f"{i}. {field}: {repr(value)}")

    def search_print_fields(self, query: str, fields: List[str], count: int = Config.DEFAULT_SEARCH_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print multiple fields from all search results.
        
        Args:
            query: Search query string
            fields: List of field names to print
            count: Number of results
            lang: Language code
            country: Country code
        """
        data = self.search_get_fields(query, fields, count, lang, country)
        for i, app_data in enumerate(data):
            try:
                field_str = ', '.join(f'{field}: {value}' for field, value in app_data.items())
                print(f"{i}. {field_str}")
            except UnicodeEncodeError:
                field_str = ', '.join(f'{field}: {repr(value)}' for field, value in app_data.items())
                print(f"{i}. {field_str}")

    def search_print_all(self, query: str, count: int = Config.DEFAULT_SEARCH_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print all search results as JSON.
        
        Args:
            query: Search query string
            count: Number of results
            lang: Language code
            country: Country code
        """
        results = self.search_analyze(query, count, lang, country)
        for i, result in enumerate(results):
            try:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            except UnicodeEncodeError:
                print(json.dumps(result, indent=2, ensure_ascii=True))


class ReviewsMethods:
    """Methods for extracting user reviews and ratings."""
    def __init__(self, http_client: str = None, proxies: ProxyConfig = None):
        """Initialize ReviewsMethods with scraper and parser.
        
        Args:
            http_client: Optional HTTP client name
            proxies: Optional proxy configuration
        """
        self.scraper = ReviewsScraper(http_client=http_client, proxies=proxies)
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

    def reviews_print_field(self, app_id: str, field: str, count: int = Config.DEFAULT_REVIEWS_COUNT,
                           lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, sort: str = Config.DEFAULT_REVIEWS_SORT) -> None:
        """Print single field from all reviews.
        
        Args:
            app_id: Google Play app ID
            field: Field name to print
            count: Number of reviews
            lang: Language code
            country: Country code
            sort: Sort order
        """
        field_values = self.reviews_get_field(app_id, field, count, lang, country, sort)
        for i, value in enumerate(field_values):
            try:
                print(f"{i+1}. {field}: {value}")
            except UnicodeEncodeError:
                print(f"{i+1}. {field}: {repr(value)}")

    def reviews_print_fields(self, app_id: str, fields: List[str], count: int = Config.DEFAULT_REVIEWS_COUNT,
                            lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, sort: str = Config.DEFAULT_REVIEWS_SORT) -> None:
        """Print multiple fields from all reviews.
        
        Args:
            app_id: Google Play app ID
            fields: List of field names to print
            count: Number of reviews
            lang: Language code
            country: Country code
            sort: Sort order
        """
        reviews_data = self.reviews_get_fields(app_id, fields, count, lang, country, sort)
        for i, review in enumerate(reviews_data):
            for field, value in review.items():
                try:
                    print(f"{field}: {value}")
                except UnicodeEncodeError:
                    print(f"{field}: {repr(value)}")

    def reviews_print_all(self, app_id: str, count: int = Config.DEFAULT_REVIEWS_COUNT, lang: str = Config.DEFAULT_LANGUAGE,
                         country: str = Config.DEFAULT_COUNTRY, sort: str = Config.DEFAULT_REVIEWS_SORT) -> None:
        """Print all reviews as JSON.
        
        Args:
            app_id: Google Play app ID
            count: Number of reviews
            lang: Language code
            country: Country code
            sort: Sort order
        """
        reviews_data = self.reviews_analyze(app_id, count, lang, country, sort)
        try:
            print(json.dumps(reviews_data, indent=2, ensure_ascii=False))
        except UnicodeEncodeError:
            print(json.dumps(reviews_data, indent=2, ensure_ascii=True))


class DeveloperMethods:
    """Methods for getting all apps from a developer."""
    def __init__(self, http_client: str = None, proxies: ProxyConfig = None):
        """Initialize DeveloperMethods with scraper and parser.
        
        Args:
            http_client: Optional HTTP client name
            proxies: Optional proxy configuration
        """
        self.scraper = DeveloperScraper(http_client=http_client, proxies=proxies)
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

    def developer_print_field(self, dev_id: str, field: str, count: int = Config.DEFAULT_DEVELOPER_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print single field from all developer apps.
        
        Args:
            dev_id: Developer ID
            field: Field name to print
            count: Number of apps
            lang: Language code
            country: Country code
        """
        values = self.developer_get_field(dev_id, field, count, lang, country)
        for i, value in enumerate(values):
            try:
                print(f"{i+1}. {field}: {value}")
            except UnicodeEncodeError:
                print(f"{i+1}. {field}: {repr(value)}")

    def developer_print_fields(self, dev_id: str, fields: List[str], count: int = Config.DEFAULT_DEVELOPER_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print multiple fields from all developer apps.
        
        Args:
            dev_id: Developer ID
            fields: List of field names to print
            count: Number of apps
            lang: Language code
            country: Country code
        """
        data = self.developer_get_fields(dev_id, fields, count, lang, country)
        for i, app_data in enumerate(data):
            try:
                field_str = ', '.join(f'{field}: {value}' for field, value in app_data.items())
                print(f"{i+1}. {field_str}")
            except UnicodeEncodeError:
                field_str = ', '.join(f'{field}: {repr(value)}' for field, value in app_data.items())
                print(f"{i+1}. {field_str}")

    def developer_print_all(self, dev_id: str, count: int = Config.DEFAULT_DEVELOPER_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print all developer apps as JSON.
        
        Args:
            dev_id: Developer ID
            count: Number of apps
            lang: Language code
            country: Country code
        """
        results = self.developer_analyze(dev_id, count, lang, country)
        try:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        except UnicodeEncodeError:
            print(json.dumps(results, indent=2, ensure_ascii=True))


class SimilarMethods:
    """Methods for finding similar/competitor apps."""
    def __init__(self, http_client: str = None, proxies: ProxyConfig = None):
        """Initialize SimilarMethods with scraper and parser.
        
        Args:
            http_client: Optional HTTP client name
            proxies: Optional proxy configuration
        """
        self.scraper = SimilarScraper(http_client=http_client, proxies=proxies)
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

    def similar_print_field(self, app_id: str, field: str, count: int = Config.DEFAULT_SIMILAR_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print single field from all similar apps.
        
        Args:
            app_id: Google Play app ID
            field: Field name to print
            count: Number of similar apps
            lang: Language code
            country: Country code
        """
        values = self.similar_get_field(app_id, field, count, lang, country)
        for i, value in enumerate(values):
            try:
                print(f"{i+1}. {field}: {value}")
            except UnicodeEncodeError:
                print(f"{i+1}. {field}: {repr(value)}")

    def similar_print_fields(self, app_id: str, fields: List[str], count: int = Config.DEFAULT_SIMILAR_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print multiple fields from all similar apps.
        
        Args:
            app_id: Google Play app ID
            fields: List of field names to print
            count: Number of similar apps
            lang: Language code
            country: Country code
        """
        data = self.similar_get_fields(app_id, fields, count, lang, country)
        for i, app_data in enumerate(data):
            try:
                field_str = ', '.join(f'{field}: {value}' for field, value in app_data.items())
                print(f"{i+1}. {field_str}")
            except UnicodeEncodeError:
                field_str = ', '.join(f'{field}: {repr(value)}' for field, value in app_data.items())
                print(f"{i+1}. {field_str}")

    def similar_print_all(self, app_id: str, count: int = Config.DEFAULT_SIMILAR_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print all similar apps as JSON.
        
        Args:
            app_id: Google Play app ID
            count: Number of similar apps
            lang: Language code
            country: Country code
        """
        results = self.similar_analyze(app_id, count, lang, country)
        try:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        except UnicodeEncodeError:
            print(json.dumps(results, indent=2, ensure_ascii=True))


class ListMethods:
    """Methods for getting top charts (free, paid, grossing)."""
    def __init__(self, http_client: str = None, proxies: ProxyConfig = None):
        """Initialize ListMethods with scraper and parser.
        
        Args:
            http_client: Optional HTTP client name
            proxies: Optional proxy configuration
        """
        self.scraper = ListScraper(http_client=http_client, proxies=proxies)
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

    def list_print_field(self, collection: str, field: str, category: str = Config.DEFAULT_LIST_CATEGORY, count: int = Config.DEFAULT_LIST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print single field from all list apps.
        
        Args:
            collection: Collection type
            field: Field name to print
            category: App category
            count: Number of apps
            lang: Language code
            country: Country code
        """
        values = self.list_get_field(collection, field, category, count, lang, country)
        for i, value in enumerate(values):
            try:
                print(f"{i+1}. {field}: {value}")
            except UnicodeEncodeError:
                print(f"{i+1}. {field}: {repr(value)}")

    def list_print_fields(self, collection: str, fields: List[str], category: str = Config.DEFAULT_LIST_CATEGORY, count: int = Config.DEFAULT_LIST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print multiple fields from all list apps.
        
        Args:
            collection: Collection type
            fields: List of field names to print
            category: App category
            count: Number of apps
            lang: Language code
            country: Country code
        """
        data = self.list_get_fields(collection, fields, category, count, lang, country)
        for i, app_data in enumerate(data):
            try:
                field_str = ', '.join(f'{field}: {value}' for field, value in app_data.items())
                print(f"{i+1}. {field_str}")
            except UnicodeEncodeError:
                field_str = ', '.join(f'{field}: {repr(value)}' for field, value in app_data.items())
                print(f"{i+1}. {field_str}")

    def list_print_all(self, collection: str = Config.DEFAULT_LIST_COLLECTION, category: str = Config.DEFAULT_LIST_CATEGORY, count: int = Config.DEFAULT_LIST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print all list apps as JSON.
        
        Args:
            collection: Collection type
            category: App category
            count: Number of apps
            lang: Language code
            country: Country code
        """
        results = self.list_analyze(collection, category, count, lang, country)
        try:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        except UnicodeEncodeError:
            print(json.dumps(results, indent=2, ensure_ascii=True))


class SuggestMethods:
    """Methods for getting search suggestions and autocomplete."""
    def __init__(self, http_client: str = None, proxies: ProxyConfig = None):
        """Initialize SuggestMethods with scraper and parser.
        
        Args:
            http_client: Optional HTTP client name
            proxies: Optional proxy configuration
        """
        self.scraper = SuggestScraper(http_client=http_client, proxies=proxies)
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

    def suggest_print_all(self, term: str, count: int = Config.DEFAULT_SUGGEST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print all suggestions as JSON.
        
        Args:
            term: Search term
            count: Number of suggestions
            lang: Language code
            country: Country code
        """
        suggestions = self.suggest_analyze(term, count, lang, country)
        try:
            print(json.dumps(suggestions, indent=2, ensure_ascii=False))
        except UnicodeEncodeError:
            print(json.dumps(suggestions, indent=2, ensure_ascii=True))

    def suggest_print_nested(self, term: str, count: int = Config.DEFAULT_SUGGEST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> None:
        """Print nested suggestions as JSON.
        
        Args:
            term: Search term
            count: Number of suggestions per level
            lang: Language code
            country: Country code
        """
        nested = self.suggest_nested(term, count, lang, country)
        try:
            print(json.dumps(nested, indent=2, ensure_ascii=False))
        except UnicodeEncodeError:
            print(json.dumps(nested, indent=2, ensure_ascii=True))
