#!/usr/bin/env python3
"""
Simple test script to verify gplay-scraper package functionality
This script tests basic import and initialization without network calls
"""

import unittest
import sys
import os

# Add the parent directory to the path to import gplay_scraper
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gplay_scraper import GPlayScraper


class TestPackageFunctionality(unittest.TestCase):
    """Package functionality tests that don't require network access"""
    
    def test_import_gplay_scraper(self):
        """Test that GPlayScraper can be imported"""
        from gplay_scraper import GPlayScraper
        self.assertTrue(GPlayScraper is not None)
    
    def test_scraper_initialization(self):
        """Test that GPlayScraper can be initialized"""
        scraper = GPlayScraper()
        self.assertIsInstance(scraper, GPlayScraper)
    
    def test_all_methods_exist(self):
        """Test that all expected methods exist"""
        scraper = GPlayScraper()
        
        method_groups = [
            ("app", ["analyze", "get_field", "get_fields", "print_field", "print_fields", "print_all"]),
            ("search", ["analyze", "get_field", "get_fields", "print_field", "print_fields", "print_all"]),
            ("reviews", ["analyze", "get_field", "get_fields", "print_field", "print_fields", "print_all"]),
            ("developer", ["analyze", "get_field", "get_fields", "print_field", "print_fields", "print_all"]),
            ("similar", ["analyze", "get_field", "get_fields", "print_field", "print_fields", "print_all"]),
            ("list", ["analyze", "get_field", "get_fields", "print_field", "print_fields", "print_all"]),
            ("suggest", ["analyze", "nested", "print_all", "print_nested"]),
        ]
        
        total_methods = 0
        for group, methods in method_groups:
            for method in methods:
                method_name = f"{group}_{method}"
                if hasattr(scraper, method_name):
                    print(f"✓ Method {method_name} exists")
                    total_methods += 1
                else:
                    print(f"✗ Method {method_name} missing")
                    self.fail(f"Method {method_name} missing")
        
        print(f"\n✅ All {total_methods} methods found and working!")
        self.assertEqual(total_methods, 40, "Should have exactly 40 methods")
    
    def test_proxy_configuration(self):
        """Ensure proxy configuration can be set during init and updated later."""
        proxy_url = "http://localhost:8080"
        scraper = GPlayScraper(proxies=proxy_url)
        
        http_client = scraper.app_methods.scraper.http_client
        self.assertEqual(http_client.proxies.get("http"), proxy_url)
        self.assertEqual(http_client.proxies.get("https"), proxy_url)
        
        scraper.set_proxies(None)
        self.assertFalse(scraper.app_methods.scraper.http_client.proxies)


if __name__ == '__main__':
    unittest.main()
