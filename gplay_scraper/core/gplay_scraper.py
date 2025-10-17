import json
import re
import logging
from typing import Dict
from ..utils.http_client import HttpClient, ProxyConfig
from ..config import Config
from ..exceptions import DataParsingError, InvalidAppIdError
from urllib.parse import quote

logger = logging.getLogger(__name__)


class AppScraper:
    """Scraper for fetching app details from Google Play Store."""
    
    def __init__(self, rate_limit_delay: float = None, http_client: str = None, proxies: ProxyConfig = None):
        """Initialize AppScraper with HTTP client.
        
        Args:
            rate_limit_delay: Delay between requests
            http_client: HTTP client name
            proxies: Optional proxy configuration
        """
        self.http_client = HttpClient(rate_limit_delay, http_client, proxies)
    
    def set_proxies(self, proxies: ProxyConfig) -> None:
        """Update proxy configuration for subsequent requests."""
        self.http_client.set_proxies(proxies)

    def fetch_playstore_page(self, app_id: str, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> str:
        """Fetch app page HTML from Google Play Store.
        
        Args:
            app_id: Google Play app ID
            lang: Language code
            country: Country code
            
        Returns:
            HTML content of app page
        """
        return self.http_client.fetch_app_page(app_id, lang, country)
    
    def fetch_fallback_data(self, app_id: str) -> Dict:
        """Fetch app data without hl/gl parameters for missing fields.
        
        Args:
            app_id: Google Play app ID
            
        Returns:
            Dictionary containing ds:5 dataset from fallback request
        """
        html_content = self.http_client.fetch_app_page_no_locale(app_id)
        
        ds_match = re.search(r'AF_initDataCallback\s*\(\s*({\s*key:\s*["\']ds:5["\'][\s\S]*?})\s*\)\s*;', html_content, re.DOTALL)
        if ds_match:
            ds5_data = ds_match.group(1)
        else:
            all_callbacks = re.findall(r'AF_initDataCallback\s*\(\s*({[\s\S]*?})\s*\)\s*;', html_content, re.DOTALL)
            ds5_data = ""
            for callback in all_callbacks:
                if "'ds:5'" in callback or '"ds:5"' in callback:
                    ds5_data = callback
                    break
        
        return {"ds:5": ds5_data} if ds5_data else None

    def scrape_play_store_data(self, app_id: str, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> Dict:
        """Extract dataset from app page HTML with fallback for missing release date.
        
        Args:
            app_id: Google Play app ID
            lang: Language code
            country: Country code
            
        Returns:
            Dictionary containing ds:5 dataset
            
        Raises:
            DataParsingError: If dataset not found
        """
        html_content = self.fetch_playstore_page(app_id, lang, country)
        
        ds_match = re.search(r'AF_initDataCallback\s*\(\s*({\s*key:\s*["\']ds:5["\'][\s\S]*?})\s*\)\s*;', html_content, re.DOTALL)
        if ds_match:
            ds5_data = ds_match.group(1)
        else:
            all_callbacks = re.findall(r'AF_initDataCallback\s*\(\s*({[\s\S]*?})\s*\)\s*;', html_content, re.DOTALL)
            ds5_data = ""
            for callback in all_callbacks:
                if "'ds:5'" in callback or '"ds:5"' in callback:
                    ds5_data = callback
                    break
        
        if not ds5_data:
            raise DataParsingError(Config.ERROR_MESSAGES["DS5_NOT_FOUND"])
        
        return {"ds:5": ds5_data, "fallback_needed": False}


class SearchScraper:
    """Scraper for fetching search results from Google Play Store."""
    
    def __init__(self, rate_limit_delay: float = None, http_client: str = None, proxies: ProxyConfig = None):
        """Initialize SearchScraper with HTTP client."""
        self.http_client = HttpClient(rate_limit_delay, http_client, proxies)
    
    def set_proxies(self, proxies: ProxyConfig) -> None:
        """Update proxy configuration for subsequent requests."""
        self.http_client.set_proxies(proxies)

    def fetch_playstore_search(self, query: str, count: int, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> str:
        """Fetch search page HTML from Google Play Store.
        
        Args:
            query: Search query string
            count: Number of results needed
            lang: Language code
            country: Country code
            
        Returns:
            HTML content of search page
            
        Raises:
            InvalidAppIdError: If query is invalid
        """
        if not query or not isinstance(query, str):
            raise InvalidAppIdError(Config.ERROR_MESSAGES["INVALID_QUERY"])
        
        if count <= 0:
            return ""
        
        return self.http_client.fetch_search_page(query=query, lang=lang, country=country)

    def scrape_play_store_data(self, query: str, count: int = Config.DEFAULT_SEARCH_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> Dict:
        """Scrape search results with automatic pagination support.
        
        Args:
            query: Search query string
            count: Total number of results to fetch
            lang: Language code
            country: Country code
            
        Returns:
            Dictionary containing all search results
            
        Raises:
            DataParsingError: If parsing fails
        """
        # Get initial search page
        html_content = self.fetch_playstore_search(query, count, lang, country)
        
        # Use parser for all parsing operations
        from .gplay_parser import SearchParser
        parser = SearchParser()
        dataset = parser.parse_html_content(html_content)
        
        # If count <= 20, return initial results
        if count <= 20:
            return dataset
        
        # Extract pagination token
        token = parser.extract_pagination_token(dataset)
        
        # Collect all results
        all_results = []
        initial_results = self._get_nested_value(dataset.get("ds:1", []), [0, 1, 0, 0, 0], [])
        all_results.extend(initial_results)
        
        # Paginate if needed and token exists
        while len(all_results) < count and token:
            needed = min(100, count - len(all_results))
            try:
                response_text = self.http_client.fetch_search_page(token=token, needed=needed, lang=lang, country=country)
                data = json.loads(response_text[5:])
                parsed_data = json.loads(data[0][2])
                
                if parsed_data:
                    paginated_results = self._get_nested_value(parsed_data, [0, 0, 0], [])
                    all_results.extend(paginated_results)
                    # Update token for next iteration
                    token = self._get_nested_value(parsed_data, [0, 0, 7, 1])
                else:
                    break
            except (json.JSONDecodeError, IndexError, KeyError, Exception):
                break
        
        # Update dataset with all results
        if "ds:1" in dataset:
            dataset["ds:1"][0][1][0][0][0] = all_results[:count]
        
        return dataset
    

    

    
    def _get_nested_value(self, data, path, default=None):
        """Safely get nested value from data structure.
        
        Args:
            data: Data structure to traverse
            path: List of keys/indices to follow
            default: Default value if path not found
            
        Returns:
            Value at path or default
        """
        try:
            for key in path:
                data = data[key]
            return data
        except (KeyError, IndexError, TypeError):
            return default


class ReviewsScraper:
    """Scraper for fetching user reviews from Google Play Store."""
    
    # Sort order mapping
    SORT_NAMES = {
        'RELEVANT': 1,  # Most relevant reviews
        'NEWEST': 2,    # Newest reviews first
        'RATING': 3     # Sorted by rating
    }
    
    def __init__(self, rate_limit_delay: float = None, http_client: str = None, proxies: ProxyConfig = None):
        """Initialize ReviewsScraper with HTTP client."""
        self.http_client = HttpClient(rate_limit_delay, http_client, proxies)
    
    def set_proxies(self, proxies: ProxyConfig) -> None:
        """Update proxy configuration for subsequent requests."""
        self.http_client.set_proxies(proxies)

    def fetch_reviews_batch(self, app_id: str, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY, 
                           sort: int = Config.DEFAULT_REVIEWS_SORT, batch_count: int = Config.DEFAULT_REVIEWS_BATCH_SIZE, token: str = None) -> str:
        """Fetch single batch of reviews from API.
        
        Args:
            app_id: Google Play app ID
            lang: Language code
            country: Country code
            sort: Sort order (NEWEST, RELEVANT, RATING)
            batch_count: Number of reviews per batch
            token: Pagination token for next batch
            
        Returns:
            Raw API response content
        """
        sort_value = self.SORT_NAMES.get(sort, sort) if isinstance(sort, str) else sort
        return self.http_client.fetch_reviews_batch(app_id, lang, country, sort_value, batch_count, token)

    def scrape_reviews_data(self, app_id: str, count: int = Config.DEFAULT_REVIEWS_COUNT, lang: str = Config.DEFAULT_LANGUAGE, 
                           country: str = Config.DEFAULT_COUNTRY, sort: int = Config.DEFAULT_REVIEWS_SORT) -> Dict:
        """Scrape multiple batches of reviews.
        
        Args:
            app_id: Google Play app ID
            count: Total number of reviews to fetch
            lang: Language code
            country: Country code
            sort: Sort order
            
        Returns:
            Dictionary containing all review responses
        """
        all_responses = []
        token = None
        batch_size = Config.DEFAULT_REVIEWS_BATCH_SIZE
        
        while len(all_responses) * batch_size < count:
            remaining = count - (len(all_responses) * batch_size)
            fetch_count = min(batch_size, remaining)
            
            response = self.fetch_reviews_batch(app_id, lang, country, sort, fetch_count, token)
            
            if not response:
                break
                
            all_responses.append(response)
            
            try:
                regex = re.compile(r"\)]}'\n\n([\s\S]+)")
                matches = regex.findall(response)
                if matches:
                    data = json.loads(matches[0])
                    token = json.loads(data[0][2])[-2][-1]
                    if not token or isinstance(token, list):
                        break
            except (json.JSONDecodeError, IndexError, KeyError):
                break
        
        return {"reviews": all_responses}


class DeveloperScraper:
    """Scraper for fetching developer portfolio from Google Play Store."""
    
    def __init__(self, rate_limit_delay: float = None, http_client: str = None, proxies: ProxyConfig = None):
        """Initialize DeveloperScraper with HTTP client."""
        self.http_client = HttpClient(rate_limit_delay, http_client, proxies)
    
    def set_proxies(self, proxies: ProxyConfig) -> None:
        """Update proxy configuration for subsequent requests."""
        self.http_client.set_proxies(proxies)

    def fetch_developer_page(self, dev_id: str, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> str:
        """Fetch developer page HTML from Google Play Store.
        
        Args:
            dev_id: Developer ID (numeric or string)
            lang: Language code
            country: Country code
            
        Returns:
            HTML content of developer page
        """
        return self.http_client.fetch_developer_page(dev_id, lang, country)

    def scrape_play_store_data(self, dev_id: str, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> Dict:
        """Extract dataset from developer page HTML.
        
        Args:
            dev_id: Developer ID
            lang: Language code
            country: Country code
            
        Returns:
            Dictionary containing ds:3 dataset and dev_id
            
        Raises:
            DataParsingError: If dataset not found
        """
        html_content = self.fetch_developer_page(dev_id, lang, country)
        
        ds_match = re.search(r'AF_initDataCallback\s*\(\s*({\s*key:\s*["\']ds:3["\'][\s\S]*?})\s*\)\s*;', html_content, re.DOTALL)
        if ds_match:
            ds3_data = ds_match.group(1)
        else:
            all_callbacks = re.findall(r'AF_initDataCallback\s*\(\s*({[\s\S]*?})\s*\)\s*;', html_content, re.DOTALL)
            ds3_data = ""
            for callback in all_callbacks:
                if "'ds:3'" in callback or '"ds:3"' in callback:
                    ds3_data = callback
                    break
        
        if not ds3_data:
            raise DataParsingError(Config.ERROR_MESSAGES["DS3_NOT_FOUND"])
        
        return {"ds:3": ds3_data, "dev_id": dev_id}


class SimilarScraper:
    """Scraper for fetching similar apps from Google Play Store."""
    
    def __init__(self, rate_limit_delay: float = None, http_client: str = None, proxies: ProxyConfig = None):
        """Initialize SimilarScraper with HTTP client."""
        self.http_client = HttpClient(rate_limit_delay, http_client, proxies)
    
    def set_proxies(self, proxies: ProxyConfig) -> None:
        """Update proxy configuration for subsequent requests."""
        self.http_client.set_proxies(proxies)

    def fetch_similar_page(self, app_id: str, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> str:
        """Fetch app page HTML to extract similar apps cluster URL.
        
        Args:
            app_id: Google Play app ID
            lang: Language code
            country: Country code
            
        Returns:
            HTML content of app page
        """
        return self.http_client.fetch_app_page(app_id, lang, country)

    def scrape_play_store_data(self, app_id: str, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> Dict:
        """Extract similar apps dataset from cluster page.
        
        Args:
            app_id: Google Play app ID
            lang: Language code
            country: Country code
            
        Returns:
            Dictionary containing ds:3 dataset
            
        Raises:
            DataParsingError: If dataset not found
        """
        html_content = self.fetch_similar_page(app_id, lang, country)
        
        # Extract cluster URL from app page
        pattern1 = r'&quot;(/store/apps/collection/cluster\?gsr=[^&]+)&quot;'
        matches1 = re.findall(pattern1, html_content)
        pattern2 = r'"(/store/apps/collection/cluster\?gsr=[^"]+)"'
        matches2 = re.findall(pattern2, html_content)
        all_matches = list(set(matches1 + matches2))
        
        if not all_matches:
            return {"ds:3": None}
        
        cluster_url = all_matches[0].replace('&amp;', '&')
        cluster_html = self.http_client.fetch_cluster_page(cluster_url, lang, country)
        
        ds_match = re.search(r'AF_initDataCallback\s*\(\s*({\s*key:\s*["\']ds:3["\'][\s\S]*?})\s*\)\s*;', cluster_html, re.DOTALL)
        if ds_match:
            ds3_data = ds_match.group(1)
        else:
            all_callbacks = re.findall(r'AF_initDataCallback\s*\(\s*({[\s\S]*?})\s*\)\s*;', cluster_html, re.DOTALL)
            ds3_data = ""
            for callback in all_callbacks:
                if "'ds:3'" in callback or '"ds:3"' in callback:
                    ds3_data = callback
                    break
        
        if not ds3_data:
            raise DataParsingError(Config.ERROR_MESSAGES["DS3_NOT_FOUND"])
        
        return {"ds:3": ds3_data}


class ListScraper:
    """Scraper for fetching top charts from Google Play Store."""

    # Collection name mapping
    CLUSTER_NAMES = {
        'TOP_FREE': 'topselling_free',      # Top free apps
        'TOP_PAID': 'topselling_paid',      # Top paid apps
        'TOP_GROSSING': 'topgrossing'       # Top grossing apps
    }
    
    def __init__(self, rate_limit_delay: float = None, http_client: str = None, proxies: ProxyConfig = None):
        """Initialize ListScraper with HTTP client."""
        self.http_client = HttpClient(rate_limit_delay, http_client, proxies)
    
    def set_proxies(self, proxies: ProxyConfig) -> None:
        """Update proxy configuration for subsequent requests."""
        self.http_client.set_proxies(proxies)

    def scrape_play_store_data(self, collection: str, category: str = Config.DEFAULT_LIST_CATEGORY, count: int = Config.DEFAULT_LIST_COUNT, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> Dict:
        """Scrape top charts data from Google Play Store.
        
        Args:
            collection: Collection type (TOP_FREE, TOP_PAID, TOP_GROSSING)
            category: App category (e.g., GAME, SOCIAL)
            count: Number of apps to fetch
            lang: Language code
            country: Country code
            
        Returns:
            Dictionary containing collection data
            
        Raises:
            DataParsingError: If JSON parsing fails
        """
        cluster = self.CLUSTER_NAMES.get(collection, collection)
        response_text = self.http_client.fetch_list_page(cluster, category, count, lang, country)
        
        try:
            lines = response_text.strip().split('\n')
            data = json.loads(lines[2])
            collection_data = json.loads(data[0][2])
            return {"collection_data": collection_data}
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            raise DataParsingError(Config.ERROR_MESSAGES["JSON_PARSE_FAILED"].format(error=str(e)))


class SuggestScraper:
    """Scraper for fetching search suggestions from Google Play Store."""
    
    def __init__(self, rate_limit_delay: float = None, http_client: str = None, proxies: ProxyConfig = None):
        """Initialize SuggestScraper with HTTP client."""
        self.http_client = HttpClient(rate_limit_delay, http_client, proxies)
    
    def set_proxies(self, proxies: ProxyConfig) -> None:
        """Update proxy configuration for subsequent requests."""
        self.http_client.set_proxies(proxies)

    def scrape_suggestions(self, term: str, lang: str = Config.DEFAULT_LANGUAGE, country: str = Config.DEFAULT_COUNTRY) -> Dict:
        """Scrape search suggestions from Google Play Store.
        
        Args:
            term: Search term for suggestions
            lang: Language code
            country: Country code
            
        Returns:
            Dictionary containing list of suggestions
            
        Raises:
            DataParsingError: If JSON parsing fails
        """
        if not term:
            return {"suggestions": []}
        
        response_text = self.http_client.fetch_suggest_page(term, lang, country)
        
        try:
            input_data = json.loads(response_text[5:])
            data = json.loads(input_data[0][2])
            
            if data is None:
                return {"suggestions": []}
            
            suggestions = [s[0] for s in data[0][0]]
            return {"suggestions": suggestions}
        except (json.JSONDecodeError, IndexError, KeyError, TypeError) as e:
            raise DataParsingError(Config.ERROR_MESSAGES["JSON_PARSE_FAILED"].format(error=str(e)))
