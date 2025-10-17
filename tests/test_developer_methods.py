"""
Unit tests for Developer Methods
"""

import unittest
import time
import warnings
from gplay_scraper import GPlayScraper
from gplay_scraper.exceptions import GPlayScraperError, NetworkError, RateLimitError


class TestDeveloperMethods(unittest.TestCase):
    """Test suite for developer methods."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.scraper = GPlayScraper()  # Initialize scraper
        self.dev_id = "5700313618786177705"  # Google Inc. developer ID
        self.count = 10  # Number of items to fetch
        self.lang = "en"  # Language
        self.country = "us"  # Country
    
    def test_developer_analyze(self):
        """Test developer_analyze returns list of apps."""
        time.sleep(2)
        try:
            result = self.scraper.developer_analyze(self.dev_id, count=self.count, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                self.assertGreater(len(result), 0)
                print(f"\n✅ Developer apps ({len(result)} apps):")
                for i, app in enumerate(result[:3]):  # Show first 3 apps
                    print(f"  {i+1}. {app.get('title', 'N/A')} - {app.get('score', 'N/A')} stars")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_developer_analyze: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_developer_get_field(self):
        """Test developer_get_field returns list of field values."""
        time.sleep(2)
        try:
            result = self.scraper.developer_get_field(self.dev_id, "title", count=self.count, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                print(f"\n✅ Developer app titles ({len(result)} apps):")
                for i, title in enumerate(result[:3]):
                    print(f"  {i+1}. {title}")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_developer_get_field: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_developer_get_fields(self):
        """Test developer_get_fields returns list of dictionaries."""
        time.sleep(2)
        try:
            result = self.scraper.developer_get_fields(self.dev_id, ["title", "score"], count=self.count, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                print(f"\n✅ Developer app fields ({len(result)} apps):")
                for i, app in enumerate(result[:3]):
                    print(f"  {i+1}. {app.get('title', 'N/A')} - {app.get('score', 'N/A')} stars")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_developer_get_fields: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_developer_print_field(self):
        """Test developer_print_field executes without error."""
        time.sleep(2)
        try:
            print(f"\n✅ developer_print_field output:")
            self.scraper.developer_print_field(self.dev_id, "title", count=self.count, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_developer_print_field: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"developer_print_field raised unexpected {e}")
    
    def test_developer_print_fields(self):
        """Test developer_print_fields executes without error."""
        time.sleep(2)
        try:
            print(f"\n✅ developer_print_fields output:")
            self.scraper.developer_print_fields(self.dev_id, ["title", "score"], count=self.count, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_developer_print_fields: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"developer_print_fields raised unexpected {e}")
    
    def test_developer_print_all(self):
        """Test developer_print_all executes without error."""
        time.sleep(2)
        try:
            print(f"\n✅ developer_print_all output:")
            self.scraper.developer_print_all(self.dev_id, count=self.count, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_developer_print_all: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"developer_print_all raised unexpected {e}")

if __name__ == '__main__':
    unittest.main()
