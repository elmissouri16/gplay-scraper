"""
Unit tests for List Methods
"""

import unittest
import time
import warnings
from gplay_scraper import GPlayScraper
from gplay_scraper.exceptions import GPlayScraperError, NetworkError, RateLimitError


class TestListMethods(unittest.TestCase):
    """Test suite for list methods (top charts)."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.scraper = GPlayScraper()  # Initialize scraper
        self.collection = "TOP_FREE"  # Top free apps collection
        self.category = "GAME"  # Game category
        self.count = 10  # Number of items to fetch
        self.lang = "en"  # Language
        self.country = "us"  # Country
    
    def test_list_analyze(self):
        """Test list_analyze returns list of top apps."""
        time.sleep(2)
        try:
            result = self.scraper.list_analyze(self.collection, self.category, count=self.count, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                self.assertGreater(len(result), 0)
                print(f"\n✅ Top {self.collection} {self.category} apps ({len(result)} apps):")
                for i, app in enumerate(result[:3]):  # Show first 3 apps
                    print(f"  {i+1}. {app.get('title', 'N/A')} - {app.get('developer', 'N/A')}")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_list_analyze: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_list_get_field(self):
        """Test list_get_field returns list of field values."""
        time.sleep(2)
        try:
            result = self.scraper.list_get_field(self.collection, self.category, "title", count=self.count, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                print(f"\n✅ Top chart app titles ({len(result)} apps):")
                for i, title in enumerate(result[:3]):
                    print(f"  {i+1}. {title}")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_list_get_field: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_list_get_fields(self):
        """Test list_get_fields returns list of dictionaries."""
        time.sleep(2)
        try:
            result = self.scraper.list_get_fields(self.collection, self.category, ["title", "score"], count=self.count, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                print(f"\n✅ Top chart app fields ({len(result)} apps):")
                for i, app in enumerate(result[:3]):
                    print(f"  {i+1}. {app.get('title', 'N/A')} - {app.get('score', 'N/A')} stars")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_list_get_fields: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_list_print_field(self):
        """Test list_print_field executes without error."""
        time.sleep(2)
        try:
            print(f"\n✅ list_print_field output:")
            self.scraper.list_print_field(self.collection, self.category, "title", count=self.count, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_list_print_field: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"list_print_field raised unexpected {e}")
    
    def test_list_print_fields(self):
        """Test list_print_fields executes without error."""
        time.sleep(2)
        try:
            print(f"\n✅ list_print_fields output:")
            self.scraper.list_print_fields(self.collection, self.category, ["title", "score"], count=self.count, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_list_print_fields: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"list_print_fields raised unexpected {e}")
    
    def test_list_print_all(self):
        """Test list_print_all executes without error."""
        time.sleep(2)
        try:
            print(f"\n✅ list_print_all output:")
            self.scraper.list_print_all(self.collection, self.category, count=self.count, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_list_print_all: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"list_print_all raised unexpected {e}")

if __name__ == '__main__':
    unittest.main()
