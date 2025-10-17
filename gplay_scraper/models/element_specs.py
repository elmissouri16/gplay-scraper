"""Element specifications for data extraction from Google Play Store.

This module defines ElementSpec class and ElementSpecs for all 7 method types.
Each spec defines how to extract specific fields from raw JSON data.
"""

from typing import Any, Callable, List, Optional
import html
from datetime import datetime
from ..utils.helpers import unescape_text
from ..config import Config


def nested_lookup(obj: Any, key_list: List) -> Any:
    """Safely navigate nested dictionary/list structure.
    
    Args:
        obj: Object to navigate
        key_list: List of keys/indices to follow
        
    Returns:
        Value at the nested location or None
    """
    current = obj
    for key in key_list:
        try:
            current = current[key]
        except (IndexError, KeyError, TypeError):
            return None
    return current


def format_image_url(url: str, size: str = None) -> str:
    """Format image URL with size parameter.
    
    Args:
        url: Base image URL
        size: Size parameter (SMALL, MEDIUM, LARGE, ORIGINAL)
        
    Returns:
        Formatted URL with size parameter
    """
    if not url:
        return None
    size_param = Config.get_image_size(size)
    return f"{url}={size_param}"


class ElementSpec:
    """Specification for extracting a single field from raw data.
    
    Attributes:
        ds_num: Dataset number (not used, kept for compatibility)
        data_map: List of keys/indices to navigate to the field
        post_processor: Optional function to process extracted value
        fallback_value: Value to return if extraction fails
    """
    
    def __init__(
        self,
        ds_num: Optional[int],
        data_map: List[int],
        post_processor: Callable = None,
        fallback_value: Any = None,
        assets: str = None,
    ):
        """Initialize ElementSpec with extraction parameters."""
        self.ds_num = ds_num
        self.data_map = data_map
        self.post_processor = post_processor
        self.fallback_value = fallback_value
        self.assets = assets

    def extract_content(self, source: dict, assets: str = None) -> Any:
        """Extract content from source using data_map.
        
        Args:
            source: Source dictionary/list
            assets: Override asset size for this extraction
            
        Returns:
            Extracted and processed value
        """
        try:
            result = nested_lookup(source, self.data_map)
            
            if self.post_processor is not None:
                try:
                    # Pass assets to post_processor if it's an image URL formatter
                    if hasattr(self.post_processor, '__name__') and 'image' in self.post_processor.__name__:
                        result = self.post_processor(result, assets or self.assets)
                    else:
                        result = self.post_processor(result)
                except Exception:
                    pass
        except (KeyError, IndexError, TypeError, AttributeError):
            result = None
            
        if result is None and self.fallback_value is not None:
            if isinstance(self.fallback_value, ElementSpec):
                result = self.fallback_value.extract_content(source, assets)
            else:
                result = self.fallback_value
        return result


class ElementSpecs:
    """Collection of element specifications for all method types.
    
    Contains specs for:
    - App: 65+ fields for app details
    - Search: Fields for search results
    - Review: Fields for user reviews
    - Developer: Fields for developer apps
    - Similar: Fields for similar apps
    - List: Fields for top chart apps
    """
    App = {
        "title": ElementSpec("raw", [1, 2, 0, 0]),
        "description": ElementSpec(
            "raw",
            [1, 2],
            lambda s: (lambda desc_text: unescape_text(desc_text) if desc_text else None)(
                nested_lookup(s, [72, 0, 0]) or nested_lookup(s, [72, 0, 1])
            ),
        ),
        "summary": ElementSpec("raw", [1, 2, 73, 0, 1], unescape_text),
        "installs": ElementSpec("raw", [1, 2, 13, 0]),
        "minInstalls": ElementSpec("raw", [1, 2, 13, 1]),
        "realInstalls": ElementSpec("raw", [1, 2, 13, 2]),
        "score": ElementSpec("raw", [1, 2, 51, 0, 1]),
        "ratings": ElementSpec("raw", [1, 2, 51, 2, 1]),
        "reviews": ElementSpec("raw", [1, 2, 51, 3, 1]),
        "histogram": ElementSpec(
            "raw",
            [1, 2, 51, 1],
            lambda container: [
                container[1][1],
                container[2][1],
                container[3][1],
                container[4][1],
                container[5][1],
            ],
            [0, 0, 0, 0, 0],
        ),
        "price": ElementSpec(
            "raw", [1, 2, 57, 0, 0, 0, 0, 1, 0, 0], lambda price: (price / 1000000) or 0
        ),
        "free": ElementSpec("raw", [1, 2, 57, 0, 0, 0, 0, 1, 0, 0], lambda s: s == 0),
        "currency": ElementSpec("raw", [1, 2, 57, 0, 0, 0, 0, 1, 0, 1]),
        "sale": ElementSpec("raw", [1, 2, 57, 0, 0, 0, 0, 14, 0, 0], bool, False),
        "originalPrice": ElementSpec("raw", [1, 2, 57, 0, 0, 0, 0, 1, 1, 0], lambda price: (price / 1000000) if price else None),
        "offersIAP": ElementSpec("raw", [1, 2, 19, 0], bool, False),
        "inAppProductPrice": ElementSpec("raw", [1, 2, 19, 0]),
        "developer": ElementSpec("raw", [1, 2, 68, 0]),
        "developerId": ElementSpec("raw", [1, 2, 68, 1, 4, 2], lambda s: s.split("id=")[1] if s and "id=" in s else None),
        "developerEmail": ElementSpec("raw", [1, 2, 69, 1, 0]),
        "developerWebsite": ElementSpec("raw", [1, 2, 69, 0, 5, 2]),
        "developerAddress": ElementSpec("raw", [1, 2, 69, 4, 2, 0]),
        "developerPhone": ElementSpec("raw", [1, 2, 69, 4, 3]),
        "privacyPolicy": ElementSpec("raw", [1, 2, 99, 0, 5, 2]),
        "genre": ElementSpec("raw", [1, 2, 79, 0, 0, 0]),
        "genreId": ElementSpec("raw", [1, 2, 79, 0, 0, 2]),
        "categories": ElementSpec("raw", [1, 2, 79, 0, 0, 0], lambda cat: [cat] if cat else [], []),
        "icon": ElementSpec("raw", [1, 2, 95, 0, 3, 2]),
        "headerImage": ElementSpec("raw", [1, 2, 96, 0, 3, 2]),
        "screenshots": ElementSpec("raw", [1, 2, 78, 0], lambda container: [item[3][2] for item in container] if container else [], []),
        "video": ElementSpec("raw", [1, 2, 100, 0, 0, 3, 2]),
        "videoImage": ElementSpec("raw", [1, 2, 100, 1, 0, 3, 2]),
        "contentRating": ElementSpec("raw", [1, 2, 9, 0]),
        "contentRatingDescription": ElementSpec("raw", [1, 2, 9, 6, 1], fallback_value=ElementSpec("raw", [1, 2, 9, 2, 1], fallback_value=ElementSpec("raw", [1, 2, 9, 0]))),
        "appId": ElementSpec("raw", [1, 2, 1, 0, 0]),
        "adSupported": ElementSpec("raw", [1, 2, 48], bool),
        "containsAds": ElementSpec("raw", [1, 2, 48], bool, False),
        "released": ElementSpec("raw", [1, 2, 10, 0]),
        "lastUpdatedOn": ElementSpec("raw", [1, 2, 145, 0, 0], fallback_value=ElementSpec("raw", [1, 2, 112, "146", 0, 0])),
        "updated": ElementSpec("raw", [1, 2, 145, 0, 1, 0]),
        "version": ElementSpec(
            "raw", [1, 2, 140, 0, 0, 0], fallback_value="Varies with device"
        ),
        "androidVersion": ElementSpec("raw", [1, 2, 140, 1, 1, 0, 0, 1], lambda x: int(float(x)) if x else None, fallback_value=ElementSpec("raw", [1, 11, 0, 1])),
        "permissions": ElementSpec("raw", [1, 2, 74], lambda perms: {
            perm[0]: [detail[1] for detail in perm[2]] if perm[2] else []
            for section in (perms[2] if perms and len(perms) > 2 else [])
            for perm in section if section and perm and perm[0]
        } if perms and len(perms) > 2 else {}),
        "dataSafety": ElementSpec("raw", [1, 2, 136], lambda data: [item[1] for item in data[1] if item and len(item) > 1] if data and len(data) > 1 and data[1] else []),
        "appBundle": ElementSpec("raw", [1, 2, 77, 0]),
        "maxandroidapi": ElementSpec("raw", [1, 2, 140, 1, 0, 0, 0]),
        "minandroidapi": ElementSpec("raw", [1, 2, 140, 1, 1, 0, 0, 0]),
        "whatsNew": ElementSpec("raw", [1, 2, 144, 1, 1], lambda x: [line.strip() for line in html.unescape(x).split('<br>') if line.strip()] if x else []),
        "available": ElementSpec("raw", [1, 2, 18, 0], bool, False),
        "url": ElementSpec("raw", [1, 2, 1, 0, 0], lambda app_id: f"https://play.google.com/store/apps/details?id={app_id}" if app_id else None),
    }
    
    Search = {
        "title": ElementSpec("raw", [2]),
        "appId": ElementSpec("raw", [12, 0]),
        "icon": ElementSpec("raw", [1, 1, 0, 3, 2]),
        "developer": ElementSpec("raw", [4, 0, 0, 0]),
        "currency": ElementSpec("raw", [7, 0, 3, 2, 1, 0, 1]),
        "price": ElementSpec("raw", [7, 0, 3, 2, 1, 0, 0], lambda price: (price / 1000000) if price else 0),
        "free": ElementSpec("raw", [7, 0, 3, 2, 1, 0, 0], lambda s: s == 0),
        "summary": ElementSpec("raw", [4, 1, 1, 1, 1], unescape_text),
        "scoreText": ElementSpec("raw", [6, 0, 2, 1, 0]),
        "score": ElementSpec("raw", [6, 0, 2, 1, 1]),
        "url": ElementSpec("raw", [12, 0], lambda app_id: f"https://play.google.com/store/apps/details?id={app_id}" if app_id else None),
    }
    
    Review = {
        "reviewId": ElementSpec("raw", [0]),
        "userName": ElementSpec("raw", [1, 0]),
        "userImage": ElementSpec("raw", [1, 1, 3, 2]),
        "content": ElementSpec("raw", [4], unescape_text),
        "score": ElementSpec("raw", [2]),
        "thumbsUpCount": ElementSpec("raw", [6]),
        "at": ElementSpec("raw", [5, 0], lambda timestamp: datetime.fromtimestamp(timestamp).isoformat() if timestamp else None),
        "appVersion": ElementSpec("raw", [10]),
    }
    
    Developer = {
        "appId": ElementSpec("raw", [0, 0]),
        "title": ElementSpec("raw", [3]),
        "icon": ElementSpec("raw", [1, 3, 2]),
        "developer": ElementSpec("raw", [14]),
        "description": ElementSpec("raw", [13, 1], unescape_text),
        "score": ElementSpec("raw", [4, 1]),
        "scoreText": ElementSpec("raw", [4, 0]),
        "price": ElementSpec("raw", [8, 1, 0, 0], lambda price: (price / 1000000) if price else 0),
        "currency": ElementSpec("raw", [8, 1, 0, 1]),
        "free": ElementSpec("raw", [8, 1, 0, 0], lambda s: s == 0),
        "url": ElementSpec("raw", [10, 4, 2], lambda path: f"https://play.google.com{path}" if path else None),
    }
    
    Similar = {
        "appId": ElementSpec("raw", [0, 0]),
        "title": ElementSpec("raw", [3]),
        "icon": ElementSpec("raw", [1, 3, 2]),
        "developer": ElementSpec("raw", [14]),
        "description": ElementSpec("raw", [13, 1], unescape_text),
        "score": ElementSpec("raw", [4, 1]),
        "scoreText": ElementSpec("raw", [4, 0]),
        "price": ElementSpec("raw", [8, 1, 0, 0], lambda price: (price / 1000000) if price else 0),
        "currency": ElementSpec("raw", [8, 1, 0, 1]),
        "free": ElementSpec("raw", [8, 1, 0, 0], lambda s: s == 0),
        "url": ElementSpec("raw", [10, 4, 2], lambda path: f"https://play.google.com{path}" if path else None),
    }
    
    List = {
        "title": ElementSpec("raw", [0, 3]),
        "appId": ElementSpec("raw", [0, 0, 0]),
        "icon": ElementSpec("raw", [0, 1, 3, 2]),
        "screenshots": ElementSpec("raw", [0, 2], lambda container: [s[3][2] for s in container if s and len(s) > 3] if container else [], []),
        "developer": ElementSpec("raw", [0, 14]),
        "genre": ElementSpec("raw", [0, 5]),
        "installs": ElementSpec("raw", [0, 15]),
        "currency": ElementSpec("raw", [0, 8, 1, 0, 1]),
        "price": ElementSpec("raw", [0, 8, 1, 0, 0], lambda price: (price / 1000000) if price else 0),
        "free": ElementSpec("raw", [0, 8, 1, 0, 0], lambda s: s == 0),
        "description": ElementSpec("raw", [0, 13, 1], unescape_text),
        "scoreText": ElementSpec("raw", [0, 4, 0]),
        "score": ElementSpec("raw", [0, 4, 1]),
        "url": ElementSpec("raw", [0, 10, 4, 2], lambda path: f"https://play.google.com{path}" if path else None),
    }