"""
Unit tests for Similar Methods
"""

import unittest
import time
import warnings
from gplay_scraper import GPlayScraper
from gplay_scraper.exceptions import GPlayScraperError, NetworkError, RateLimitError


class TestSimilarMethods(unittest.TestCase):
    """Test suite for similar methods (find related apps)."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.scraper = GPlayScraper()  # Initialize scraper
        self.app_id = "com.whatsapp"  # WhatsApp app ID for testing
        self.count = 10  # Number of items to fetch
        self.lang = "en"  # Language
        self.country = "us"  # Country
    
    def test_similar_analyze(self):
        """Test similar_analyze returns list of similar apps."""
        time.sleep(2)
        try:
            result = self.scraper.similar_analyze(self.app_id, count=self.count, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                self.assertGreater(len(result), 0)
                print(f"\n✅ Similar apps to {self.app_id} ({len(result)} apps):")
                for i, app in enumerate(result[:3]):  # Show first 3 apps
                    print(f"  {i+1}. {app.get('title', 'N/A')} - {app.get('developer', 'N/A')}")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_similar_analyze: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_similar_get_field(self):
        """Test similar_get_field returns list of field values."""
        time.sleep(2)
        try:
            result = self.scraper.similar_get_field(self.app_id, "title", count=self.count, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                print(f"\n✅ Similar app titles ({len(result)} apps):")
                for i, title in enumerate(result[:3]):
                    print(f"  {i+1}. {title}")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_similar_get_field: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_similar_get_fields(self):
        """Test similar_get_fields returns list of dictionaries."""
        time.sleep(2)
        try:
            result = self.scraper.similar_get_fields(self.app_id, ["title", "score"], count=self.count, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                print(f"\n✅ Similar app fields ({len(result)} apps):")
                for i, app in enumerate(result[:3]):
                    print(f"  {i+1}. {app.get('title', 'N/A')} - {app.get('score', 'N/A')} stars")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_similar_get_fields: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_similar_print_field(self):
        """Test similar_print_field executes without error."""
        time.sleep(2)
        try:
            print(f"\n✅ similar_print_field output:")
            self.scraper.similar_print_field(self.app_id, "title", count=self.count, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_similar_print_field: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"similar_print_field raised unexpected {e}")
    
    def test_similar_print_fields(self):
        """Test similar_print_fields executes without error."""
        time.sleep(2)
        try:
            print(f"\n✅ similar_print_fields output:")
            self.scraper.similar_print_fields(self.app_id, ["title", "score"], count=self.count, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_similar_print_fields: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"similar_print_fields raised unexpected {e}")
    
    def test_similar_print_all(self):
        """Test similar_print_all executes without error."""
        time.sleep(2)
        try:
            print(f"\n✅ similar_print_all output:")
            self.scraper.similar_print_all(self.app_id, count=self.count, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_similar_print_all: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"similar_print_all raised unexpected {e}")

if __name__ == '__main__':
    unittest.main()
