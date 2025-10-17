import unittest
import sys
import os

# Add the parent directory to the path to import gplay_scraper
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gplay_scraper import GPlayScraper


class TestBasicFunctionality(unittest.TestCase):
    """Basic tests that don't require network access"""
    
    def test_import_gplay_scraper(self):
        """Test that GPlayScraper can be imported"""
        from gplay_scraper import GPlayScraper
        self.assertTrue(GPlayScraper is not None)
    
    def test_scraper_initialization(self):
        """Test that GPlayScraper can be initialized"""
        scraper = GPlayScraper()
        self.assertIsInstance(scraper, GPlayScraper)
    
    def test_scraper_has_required_methods(self):
        """Test that GPlayScraper has all required methods"""
        scraper = GPlayScraper()
        
        # App methods
        self.assertTrue(hasattr(scraper, 'app_analyze'))
        self.assertTrue(hasattr(scraper, 'app_get_field'))
        self.assertTrue(hasattr(scraper, 'app_get_fields'))
        self.assertTrue(hasattr(scraper, 'app_print_field'))
        self.assertTrue(hasattr(scraper, 'app_print_fields'))
        self.assertTrue(hasattr(scraper, 'app_print_all'))
        
        # Search methods
        self.assertTrue(hasattr(scraper, 'search_analyze'))
        self.assertTrue(hasattr(scraper, 'search_get_field'))
        self.assertTrue(hasattr(scraper, 'search_get_fields'))
        self.assertTrue(hasattr(scraper, 'search_print_field'))
        self.assertTrue(hasattr(scraper, 'search_print_fields'))
        self.assertTrue(hasattr(scraper, 'search_print_all'))
        
        # Reviews methods
        self.assertTrue(hasattr(scraper, 'reviews_analyze'))
        self.assertTrue(hasattr(scraper, 'reviews_get_field'))
        self.assertTrue(hasattr(scraper, 'reviews_get_fields'))
        self.assertTrue(hasattr(scraper, 'reviews_print_field'))
        self.assertTrue(hasattr(scraper, 'reviews_print_fields'))
        self.assertTrue(hasattr(scraper, 'reviews_print_all'))
        
        # Developer methods
        self.assertTrue(hasattr(scraper, 'developer_analyze'))
        self.assertTrue(hasattr(scraper, 'developer_get_field'))
        self.assertTrue(hasattr(scraper, 'developer_get_fields'))
        self.assertTrue(hasattr(scraper, 'developer_print_field'))
        self.assertTrue(hasattr(scraper, 'developer_print_fields'))
        self.assertTrue(hasattr(scraper, 'developer_print_all'))
        
        # List methods
        self.assertTrue(hasattr(scraper, 'list_analyze'))
        self.assertTrue(hasattr(scraper, 'list_get_field'))
        self.assertTrue(hasattr(scraper, 'list_get_fields'))
        self.assertTrue(hasattr(scraper, 'list_print_field'))
        self.assertTrue(hasattr(scraper, 'list_print_fields'))
        self.assertTrue(hasattr(scraper, 'list_print_all'))
        
        # Similar methods
        self.assertTrue(hasattr(scraper, 'similar_analyze'))
        self.assertTrue(hasattr(scraper, 'similar_get_field'))
        self.assertTrue(hasattr(scraper, 'similar_get_fields'))
        self.assertTrue(hasattr(scraper, 'similar_print_field'))
        self.assertTrue(hasattr(scraper, 'similar_print_fields'))
        self.assertTrue(hasattr(scraper, 'similar_print_all'))
        
        # Suggest methods (only 4 methods, not 6)
        self.assertTrue(hasattr(scraper, 'suggest_analyze'))
        self.assertTrue(hasattr(scraper, 'suggest_nested'))
        self.assertTrue(hasattr(scraper, 'suggest_print_all'))
        self.assertTrue(hasattr(scraper, 'suggest_print_nested'))


if __name__ == '__main__':
    unittest.main()
