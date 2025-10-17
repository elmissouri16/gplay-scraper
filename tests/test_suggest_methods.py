"""
Unit tests for Suggest Methods
"""

import unittest
import time
import warnings
from gplay_scraper import GPlayScraper
from gplay_scraper.exceptions import GPlayScraperError, NetworkError, RateLimitError


class TestSuggestMethods(unittest.TestCase):
    """Test suite for suggest methods (search suggestions)."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.scraper = GPlayScraper()  # Initialize scraper
        self.term = "fitness"  # Search term for testing
        self.count = 10  # Number of items to fetch
        self.lang = "en"  # Language
        self.country = "us"  # Country
    
    def test_suggest_analyze(self):
        """Test suggest_analyze returns list of suggestions."""
        time.sleep(2)
        try:
            result = self.scraper.suggest_analyze(self.term, count=self.count, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                self.assertGreater(len(result), 0)
                print(f"\n✅ Search suggestions for '{self.term}' ({len(result)} suggestions):")
                for i, suggestion in enumerate(result):
                    print(f"  {i+1}. {suggestion}")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_suggest_analyze: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_suggest_nested(self):
        """Test suggest_nested returns nested suggestions."""
        time.sleep(2)
        try:
            result = self.scraper.suggest_nested(self.term, count=self.count, lang=self.lang, country=self.country)
            self.assertIsInstance(result, dict)
            if result:
                print(f"\n✅ Nested suggestions for '{self.term}':")
                for key, suggestions in list(result.items())[:2]:  # Show first 2 nested
                    print(f"  '{key}' -> {suggestions[:3]}")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_suggest_nested: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_suggest_print_nested(self):
        """Test suggest_print_nested executes without error."""
        time.sleep(2)
        try:
            print(f"\n✅ suggest_print_nested output:")
            self.scraper.suggest_print_nested(self.term, count=self.count, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_suggest_print_nested: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"suggest_print_nested raised unexpected {e}")
    
    def test_suggest_print_all(self):
        """Test suggest_print_all executes without error."""
        time.sleep(2)
        try:
            print(f"\n✅ suggest_print_all output:")
            self.scraper.suggest_print_all(self.term, count=self.count, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_suggest_print_all: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"suggest_print_all raised unexpected {e}")

if __name__ == '__main__':
    unittest.main()
