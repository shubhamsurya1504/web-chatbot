import unittest
from unittest.mock import patch, Mock, mock_open
import tempfile
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import warnings
import urllib3
from pathlib import Path
import sys

# Add parent directory to Python path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from src.crawler import (
    HyperlinkParser,
    get_hyperlinks,
    get_domain_hyperlinks,
    crawl
)
class TestCrawler(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Suppress SSL verification warnings during tests
        warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)
        
        # Test URLs and content
        self.test_url = "https://help.slack.com"
        self.test_domain = "help.slack.com"
        
        # Create temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        self.text_dir = os.path.join(self.temp_dir, "text", self.test_domain)
        os.makedirs(self.text_dir, exist_ok=True)

    def tearDown(self):
        """Clean up after each test method."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_hyperlink_parser(self):
        """Test the HyperlinkParser class."""
        parser = HyperlinkParser()
        test_html = """
        <html>
            <body>
                <a href="https://help.slack.com/page1">Link 1</a>
                <a href="/relative/path">Link 2</a>
                <a href="mailto:test@slack.com">Email</a>
                <a href="#section">Section</a>
            </body>
        </html>
        """
        parser.feed(test_html)
        
        # Verify extracted links
        self.assertEqual(len(parser.hyperlinks), 4)
        self.assertIn("https://help.slack.com/page1", parser.hyperlinks)
        self.assertIn("/relative/path", parser.hyperlinks)
        self.assertIn("mailto:test@slack.com", parser.hyperlinks)
        self.assertIn("#section", parser.hyperlinks)

    
    @patch('urllib.request.urlopen')
    def test_get_hyperlinks(self, mock_urlopen):
        """Test the get_hyperlinks function."""
        # Create a mock response object with proper content type
        mock_response = Mock()
        mock_response.info.return_value = Mock(**{
            'get.return_value': 'text/html; charset=utf-8'
        })
        
        # Create test HTML content
        html_content = """
        <html>
            <body>
                <a href="https://help.slack.com/test">Test Link</a>
            </body>
        </html>
        """.encode('utf-8')
        
        # Configure mock response
        mock_response.read.return_value = html_content
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        # Test getting links
        links = get_hyperlinks("https://help.slack.com")
        
        # Verify results
        self.assertEqual(len(links), 1, "Expected one link to be extracted")
        self.assertIn("https://help.slack.com/test", links, "Expected link not found")
        
        # Verify mock was called correctly
        mock_urlopen.assert_called_once()
        def test_get_domain_hyperlinks(self):
            """Test the get_domain_hyperlinks function."""
            test_html = """
            <html>
                <body>
                    <a href="https://help.slack.com/page1">Internal Link</a>
                    <a href="https://other-domain.com">External Link</a>
                    <a href="/relative/path">Relative Link</a>
                    <a href="#section">Section Link</a>
                    <a href="mailto:test@slack.com">Email Link</a>
                </body>
            </html>
            """
            
            # Get domain-specific links
            local_domain = "help.slack.com"
            clean_links = get_domain_hyperlinks(local_domain, self.test_url)
            
            # Verify only internal links are included
            for link in clean_links:
                self.assertEqual(urlparse(link).netloc, local_domain)

    @patch('requests.get')
    def test_crawl_basic_functionality(self, mock_get):
        """Test basic crawling functionality."""
        # Mock response
        mock_response = Mock()
        mock_response.text = "<html><body><p>Test content</p></body></html>"
        mock_get.return_value = mock_response
        
        # Run crawl with minimal settings
        result = crawl(self.test_url, max_pages=1, max_depth=1)
        
        # Verify results
        self.assertEqual(result, self.test_domain)
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_crawl_depth_limit(self, mock_get):
        """Test crawling depth limit."""
        mock_response = Mock()
        mock_response.text = """
        <html><body>
            <a href="https://help.slack.com/page1">Link 1</a>
            <a href="https://help.slack.com/page2">Link 2</a>
        </body></html>
        """
        mock_get.return_value = mock_response
        
        # Run crawl with depth limit
        result = crawl(self.test_url, max_pages=10, max_depth=1)
        
        # Should only crawl the initial page due to depth limit
        self.assertEqual(mock_get.call_count, 1)

    @patch('requests.get')
    def test_crawl_page_limit(self, mock_get):
        """Test crawling page limit."""
        mock_response = Mock()
        mock_response.text = """
        <html><body>
            <a href="https://help.slack.com/page1">Link 1</a>
            <a href="https://help.slack.com/page2">Link 2</a>
        </body></html>
        """
        mock_get.return_value = mock_response
        
        # Run crawl with page limit
        result = crawl(self.test_url, max_pages=2, max_depth=3)
        
        # Should stop after max_pages
        self.assertLessEqual(mock_get.call_count, 2)

    @patch('requests.get')
    def test_crawl_error_handling(self, mock_get):
        """Test crawling error handling."""
        # Mock request to raise an exception
        mock_get.side_effect = Exception("Test error")
        
        # Run crawl
        result = crawl(self.test_url, max_pages=1, max_depth=1)
        
        # Should complete despite error
        self.assertEqual(result, self.test_domain)

    @patch('requests.get')
    def test_content_saving(self, mock_get):
        """Test content saving functionality."""
        # Mock response
        test_content = "Test page content"
        mock_response = Mock()
        mock_response.text = f"<html><body>{test_content}</body></html>"
        mock_get.return_value = mock_response
        
        # Use a real temporary directory for this test
        with patch('builtins.open', mock_open()) as mock_file:
            result = crawl(self.test_url, max_pages=1, max_depth=1)
            
            # Verify file operations
            mock_file.assert_called()
            handle = mock_file()
            
            # Verify content was processed by BeautifulSoup
            handle.write.assert_called()
            written_content = handle.write.call_args[0][0]
            self.assertIn(test_content, written_content)

if __name__ == '__main__':
    unittest.main(verbosity=2)