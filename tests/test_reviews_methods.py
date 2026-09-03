"""
Unit tests for Reviews Methods
"""

import json
import time
import unittest
import warnings

from gplay_scraper import GPlayScraper
from gplay_scraper.core.gplay_parser import ReviewsParser
from gplay_scraper.exceptions import GPlayScraperError, NetworkError, RateLimitError


class TestReviewsParser(unittest.TestCase):
    """Deterministic tests for Google Play review response parsing."""

    def test_parse_reviews_response_with_actual_newline_prefix(self):
        """Parse batchexecute responses containing real newline separators."""
        review_raw = [
            "review-id",
            ["Reviewer"],
            3,
            None,
            "Useful review",
            [1700000000],
            4,
            None,
            None,
            None,
            "1.2.3",
        ]
        reviews_data = [[review_raw], [None, "next-page-token"], [None]]
        response_data = [["wrb.fr", "oCPfdb", json.dumps(reviews_data)]]
        response = ")]}'\n\n" + json.dumps(response_data)

        reviews, next_token = ReviewsParser().parse_reviews_response(response)

        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0]["reviewId"], "review-id")
        self.assertEqual(reviews[0]["userName"], "Reviewer")
        self.assertEqual(reviews[0]["score"], 3)
        self.assertEqual(reviews[0]["content"], "Useful review")
        self.assertEqual(reviews[0]["thumbsUpCount"], 4)
        self.assertEqual(reviews[0]["appVersion"], "1.2.3")
        self.assertEqual(next_token, "next-page-token")


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
    
if __name__ == '__main__':
    unittest.main()
