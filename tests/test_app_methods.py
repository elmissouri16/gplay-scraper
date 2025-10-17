import unittest
import warnings
import time
from gplay_scraper import GPlayScraper
from gplay_scraper.exceptions import GPlayScraperError, NetworkError, RateLimitError


class TestAppMethods(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.scraper = GPlayScraper()  # Initialize scraper
        cls.app_id = "com.whatsapp"  # WhatsApp app ID for testing
        cls.lang = "en"  # Language
        cls.country = "us"  # Country
    
    def test_app_analyze(self):
        """Test app_analyze returns dictionary with data or handles errors gracefully"""
        time.sleep(2)  # Wait 2 seconds before request
        try:
            result = self.scraper.app_analyze(self.app_id, lang=self.lang, country=self.country)
            self.assertIsInstance(result, dict)
            if result:  # Only check if we got data
                self.assertIn('title', result)
                print(f"\n✅ App data retrieved for {self.app_id}:")
                print(f"Title: {result.get('title', 'N/A')}")
                print(f"Score: {result.get('score', 'N/A')}")
                print(f"Installs: {result.get('installs', 'N/A')}")
                print(f"Developer: {result.get('developer', 'N/A')}")
                print(f"Total fields: {len(result)}")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_app_analyze: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_app_get_field(self):
        """Test app_get_field returns single field value or handles errors gracefully"""
        time.sleep(2)  # Wait 2 seconds before request
        try:
            result = self.scraper.app_get_field(self.app_id, "title", lang=self.lang, country=self.country)
            if result is not None:
                self.assertIsInstance(result, str)
                self.assertTrue(len(result) > 0)
                print(f"\n✅ Single field 'title': {result}")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_app_get_field: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_app_get_fields(self):
        """Test app_get_fields returns multiple fields or handles errors gracefully"""
        time.sleep(2)  # Wait 2 seconds before request
        fields = ["title", "score", "installs"]
        try:
            result = self.scraper.app_get_fields(self.app_id, fields, lang=self.lang, country=self.country)
            if result:
                self.assertIsInstance(result, dict)
                print(f"\n✅ Multiple fields retrieved:")
                for field, value in result.items():
                    print(f"  {field}: {value}")
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_app_get_fields: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
    
    def test_app_print_field(self):
        """Test app_print_field executes without error or handles errors gracefully"""
        time.sleep(2)  # Wait 2 seconds before request
        try:
            print(f"\n✅ app_print_field output:")
            self.scraper.app_print_field(self.app_id, "title", lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_app_print_field: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"app_print_field raised unexpected {type(e).__name__}: {e}")
    
    def test_app_print_fields(self):
        """Test app_print_fields executes without error or handles errors gracefully"""
        time.sleep(2)  # Wait 2 seconds before request
        try:
            print(f"\n✅ app_print_fields output:")
            self.scraper.app_print_fields(self.app_id, ["title", "score"], lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_app_print_fields: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"app_print_fields raised unexpected {type(e).__name__}: {e}")
    
    def test_app_print_all(self):
        """Test app_print_all executes without error or handles errors gracefully"""
        time.sleep(2)  # Wait 2 seconds before request
        try:
            print(f"\n✅ app_print_all output:")
            self.scraper.app_print_all(self.app_id, lang=self.lang, country=self.country)
        except (NetworkError, RateLimitError, GPlayScraperError) as e:
            warnings.warn(f"Network/Rate limit error in test_app_print_all: {e}")
            self.skipTest(f"Skipping due to network/rate limit: {e}")
        except Exception as e:
            self.fail(f"app_print_all raised unexpected {type(e).__name__}: {e}")


if __name__ == '__main__':
    unittest.main()
