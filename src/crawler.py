import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Regex pattern to match a valid filename
INVALID_FILENAME_CHARS = r'[<>:"/\\|?*]'

def sanitize_filename(filename):
    """
    Remove or replace invalid characters in a filename.
    """
    return re.sub(INVALID_FILENAME_CHARS, '_', filename)

def crawl(url):
    """
    Crawl a single webpage and save its content.

    Args:
        url (str): The URL to crawl.

    Returns:
        str: The domain name of the crawled website.
    """
    local_domain = urlparse(url).netloc

    # Create necessary directories
    os.makedirs("text", exist_ok=True)
    os.makedirs(f"text/{local_domain}", exist_ok=True)
    os.makedirs("processed", exist_ok=True)

    print(f"\nCrawling: {url}")

    try:
        # Get the page content
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for HTTP status codes >= 400
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        # Skip if JavaScript is required
        if "You need to enable JavaScript to run this app." in text:
            print(f"JavaScript required for: {url}")
            return

        # Create filename from URL
        filename = sanitize_filename(url[8:].replace("/", "_"))
        if len(filename) > 100:  # Limit filename length
            filename = filename[:100]

        # Save the content
        file_path = f'text/{local_domain}/{filename}.txt'
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(text)

        print(f"Content saved to: {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"HTTP request error for {url}: {str(e)}")
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")

    print(f"Crawling completed for: {url}")
    return local_domain


# if __name__ == "__main__":
#     # Example usage
#     test_url = "https://example.com"  # Replace with your desired URL
#     domain = crawl(test_url)
#     print(f"Content saved for domain: {domain}")
