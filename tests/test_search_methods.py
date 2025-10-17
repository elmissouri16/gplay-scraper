"""
Unit tests for Search Methods
"""

import unittest
import time
import warnings
from gplay_scraper import GPlayScraper
from gplay_scraper.exceptions import GPlayScraperError, NetworkError, RateLimitError


class TestSearchMethods(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.scraper = GPlayScraper()  # Initialize scraper
        cls.query = "social media"  # Search query
        cls.count = 10  # Number of items to fetch
        cls.lang = "en"  # Language
        cls.country = "us"  # Country
    
    def test_search_analyze(self):
        """Test search_analyze returns list of results"""
        time.sleep(2)
        try:
            result = self.scraper.search_analyze(self.query, count=self.count, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                self.assertGreater(len(result), 0)
                self.assertIn('title', result[0])
                print(f"\n✅ Search results for '{self.query}' ({len(result)} apps):")
                for i, app in enumerate(result[:3]):  # Show first 3 results
                    print(f"  {i+1}. {app.get('title', 'N/A')} - {app.get('developer', 'N/A')}")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_search_analyze: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_search_get_field(self):
        """Test search_get_field returns list of field values"""
        time.sleep(2)
        try:
            result = self.scraper.search_get_field(self.query, "title", count=self.count, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                self.assertGreater(len(result), 0)
                print(f"\n✅ App titles from search ({len(result)} results):")
                for i, title in enumerate(result[:3]):
                    print(f"  {i+1}. {title}")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_search_get_field: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_search_get_fields(self):
        """Test search_get_fields returns list of dictionaries"""
        time.sleep(2)
        fields = ["title", "score"]
        try:
            result = self.scraper.search_get_fields(self.query, fields, count=self.count, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                self.assertGreater(len(result), 0)
                for field in fields:
                    self.assertIn(field, result[0])
                print(f"\n✅ Multiple fields from search ({len(result)} results):")
                for i, app in enumerate(result[:3]):
                    print(f"  {i+1}. {app.get('title', 'N/A')} - Score: {app.get('score', 'N/A')}")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_search_get_fields: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_search_print_field(self):
        """Test search_print_field executes without error"""
        time.sleep(2)
        try:
            print(f"\n✅ search_print_field output for '{self.query}':")
            self.scraper.search_print_field(self.query, "title", count=self.count, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_search_print_field: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"search_print_field raised unexpected {type(e).__name__}: {e}")
    
    def test_search_print_fields(self):
        """Test search_print_fields executes without error"""
        time.sleep(2)
        try:
            print(f"\n✅ search_print_fields output for '{self.query}':")
            self.scraper.search_print_fields(self.query, ["title", "score"], count=self.count, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_search_print_fields: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"search_print_fields raised unexpected {type(e).__name__}: {e}")
    
    def test_search_print_all(self):
        """Test search_print_all executes without error"""
        time.sleep(2)
        try:
            print(f"\n✅ search_print_all output for '{self.query}':")
            self.scraper.search_print_all(self.query, count=self.count, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_search_print_all: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"search_print_all raised unexpected {type(e).__name__}: {e}")


if __name__ == '__main__':
    unittest.main()
