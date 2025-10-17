"""Configuration module for GPlay Scraper.

Contains all constants, default values, URLs, and error messages.
"""

from typing import Dict


class Config:
    """Configuration class containing all settings and constants."""
    # HTTP request settings
    DEFAULT_TIMEOUT = 30  # Request timeout in seconds
    RATE_LIMIT_DELAY = 1.0  # Delay between requests in seconds
      
    # Google Play Store URLs
    PLAY_STORE_BASE_URL = "https://play.google.com"
    APP_DETAILS_ENDPOINT = "/store/apps/details"  # App details page
    BATCHEXECUTE_ENDPOINT = "/_/PlayStoreUi/data/batchexecute"  # Batch API endpoint
    DEVELOPER_NUMERIC_ENDPOINT = "/store/apps/dev"  # Developer page (numeric ID)
    DEVELOPER_STRING_ENDPOINT = "/store/apps/developer"  # Developer page (string ID)
    
    # Default parameters
    DEFAULT_LANGUAGE = "en"  # Default language code
    DEFAULT_COUNTRY = "us"  # Default country code
    DEFAULT_REVIEWS_SORT = "NEWEST"  # Options: NEWEST, RELEVANT, RATING
    
    # Default collection and category for list methods
    DEFAULT_LIST_COLLECTION = "TOP_FREE"  # Options: TOP_FREE, TOP_PAID, TOP_GROSSING
    DEFAULT_LIST_CATEGORY = "APPLICATION"  # Default category
    
    # Default count values for different methods
    DEFAULT_LIST_COUNT = 100  # Number of apps to fetch from lists
    DEFAULT_REVIEWS_COUNT = 100  # Number of reviews to fetch
    DEFAULT_REVIEWS_BATCH_SIZE = 50  # Reviews per batch request
    DEFAULT_SUGGEST_COUNT = 5  # Number of suggestions to fetch
    DEFAULT_SIMILAR_COUNT = 100  # Number of similar apps to fetch
    DEFAULT_DEVELOPER_COUNT = 100  # Number of developer apps to fetch
    DEFAULT_SEARCH_COUNT = 100  # Number of search results to fetch
    
    # Image size configurations
    IMAGE_SIZES = {
        "SMALL": "w512",    # 512px width
        "MEDIUM": "w1024",  # 1024px width  
        "LARGE": "w2048",   # 2048px width
        "ORIGINAL": "w9999" # Original/max size
    }
    DEFAULT_IMAGE_SIZE = "MEDIUM"  # Default image size
    
    # Error message templates
    ERROR_MESSAGES = {
        "INVALID_APP_ID": "app_id must be a non-empty string",
        "INVALID_DEV_ID": "dev_id must be a non-empty string",
        "INVALID_QUERY": "query must be a non-empty string",
        "NO_DS5_DATA": "No data found in dataset",
        "DS5_NOT_FOUND": "Could not find data",
        "JSON_PARSE_FAILED": "Failed to parse JSON: {error}",
        "APP_FETCH_FAILED": "Failed to fetch app page for {app_id}: {error}",
        "SEARCH_FETCH_FAILED": "Failed to fetch search results for '{query}': {error}",
        "REVIEWS_FETCH_FAILED": "Failed to fetch reviews batch for {app_id}: {error}",
        "REVIEWS_SCRAPE_FAILED": "Failed to scrape reviews for {app_id}: {error}",
        "DEVELOPER_FETCH_FAILED": "Failed to fetch developer page for {dev_id}: {error}",
        "CLUSTER_FETCH_FAILED": "Failed to fetch cluster page: {error}",
        "LIST_FETCH_FAILED": "Failed to fetch list page: {error}",
        "SUGGEST_FETCH_FAILED": "Failed to fetch suggestions for '{term}': {error}",
        "RATE_LIMIT_SLEEP": "Rate limiting: sleeping for {sleep_time:.2f} seconds",
        "HTTP_CLIENT_NOT_AVAILABLE": "{client} not available",
        "HTTP_ERROR": "HTTP {status_code} Error",
        "NO_HTTP_CLIENT": "No HTTP client libraries found",
        "UNKNOWN_CLIENT_TYPE": "Unknown client type: {client_type}. Supported option: curl_cffi",
        "APP_NOT_FOUND": "App not found: {app_id}",
        "SEARCH_NOT_FOUND": "Search not found: {query}",
        "REVIEWS_NOT_FOUND": "Reviews not found for app: {app_id}",
        "DEVELOPER_NOT_FOUND": "Developer not found: {dev_id}",
        "CLUSTER_NOT_FOUND": "Cluster not found: {cluster_url}",
        "LIST_NOT_FOUND": "List not found: {collection}/{category}",
        "SUGGEST_NOT_FOUND": "Suggestions not found for: {term}",
        "NO_DS3_DATA": "No data found in dataset",
        "DS3_NOT_FOUND": "Could not find data",
        "DS3_JSON_PARSE_FAILED": "Failed to parse JSON: {error}",
        "SEARCH_PAGINATION_FAILED": "Failed to fetch paginated search results: {error}"
    }
    
    @classmethod
    def get_headers(cls, user_agent: str = None) -> Dict[str, str]:
        """Generate HTTP headers optionally including a custom user agent.
        
        Args:
            user_agent: Optional custom user agent string
            
        Returns:
            Dictionary containing HTTP headers
        """
        headers: Dict[str, str] = {}
        if user_agent:
            headers["User-Agent"] = user_agent
        return headers
    
    @classmethod
    def get_image_size(cls, size: str = None) -> str:
        """Get image size parameter.
        
        Args:
            size: Size name (SMALL, MEDIUM, LARGE, ORIGINAL) or None for default
            
        Returns:
            Image size parameter string
        """
        size = size or cls.DEFAULT_IMAGE_SIZE
        return cls.IMAGE_SIZES.get(size.upper(), cls.IMAGE_SIZES[cls.DEFAULT_IMAGE_SIZE])
