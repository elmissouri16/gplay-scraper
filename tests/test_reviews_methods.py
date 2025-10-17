"""
Unit tests for Reviews Methods
"""

import unittest
import time
import warnings
from gplay_scraper import GPlayScraper
from gplay_scraper.exceptions import GPlayScraperError, NetworkError, RateLimitError


class TestReviewsMethods(unittest.TestCase):
    """Test suite for reviews methods."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.scraper = GPlayScraper()  # Initialize scraper
        self.app_id = "com.whatsapp"  # WhatsApp app ID for testing
        self.count = 10  # Number of items to fetch
        self.lang = "en"  # Language
        self.country = "us"  # Country
        self.sort = "NEWEST"  # Sort order for reviews
    
    def test_reviews_analyze(self):
        """Test reviews_analyze returns list of reviews."""
        time.sleep(2)
        try:
            result = self.scraper.reviews_analyze(self.app_id, count=self.count, sort=self.sort, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                self.assertGreater(len(result), 0)
                print(f"\n✅ Reviews for {self.app_id} ({len(result)} reviews):")
                for i, review in enumerate(result[:2]):  # Show first 2 reviews
                    print(f"  {i+1}. {review.get('userName', 'Anonymous')} - {review.get('score', 'N/A')} stars")
                    print(f"     {review.get('content', 'No content')[:100]}...")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_reviews_analyze: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_reviews_get_field(self):
        """Test reviews_get_field returns list of field values."""
        time.sleep(2)
        try:
            result = self.scraper.reviews_get_field(self.app_id, "userName", count=self.count, sort=self.sort, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                print(f"\n✅ Review usernames ({len(result)} reviews):")
                for i, username in enumerate(result[:3]):
                    print(f"  {i+1}. {username or 'Anonymous'}")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_reviews_get_field: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_reviews_get_fields(self):
        """Test reviews_get_fields returns list of dictionaries."""
        time.sleep(2)
        try:
            result = self.scraper.reviews_get_fields(self.app_id, ["userName", "score"], count=self.count, sort=self.sort, lang=self.lang, country=self.country)
            self.assertIsInstance(result, list)
            if result:
                print(f"\n✅ Review fields ({len(result)} reviews):")
                for i, review in enumerate(result[:3]):
                    print(f"  {i+1}. {review.get('userName', 'Anonymous')} - {review.get('score', 'N/A')} stars")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_reviews_get_fields: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_reviews_print_field(self):
        """Test reviews_print_field executes without error."""
        time.sleep(2)
        try:
            print(f"\n✅ reviews_print_field output:")
            self.scraper.reviews_print_field(self.app_id, "userName", count=self.count, sort=self.sort, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_reviews_print_field: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"reviews_print_field raised unexpected {e}")
    
    def test_reviews_print_fields(self):
        """Test reviews_print_fields executes without error."""
        time.sleep(2)
        try:
            print(f"\n✅ reviews_print_fields output:")
            self.scraper.reviews_print_fields(self.app_id, ["userName", "score"], count=self.count, sort=self.sort, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_reviews_print_fields: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"reviews_print_fields raised unexpected {e}")
    
    def test_reviews_print_all(self):
        """Test reviews_print_all executes without error."""
        time.sleep(2)
        try:
            print(f"\n✅ reviews_print_all output:")
            self.scraper.reviews_print_all(self.app_id, count=self.count, sort=self.sort, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_reviews_print_all: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"reviews_print_all raised unexpected {e}")

if __name__ == '__main__':
    unittest.main()
