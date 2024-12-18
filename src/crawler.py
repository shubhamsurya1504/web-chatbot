import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse
import os
import time

# Regex pattern to match a URL
HTTP_URL_PATTERN = r'^http[s]*://.+'

class HyperlinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hyperlinks = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.hyperlinks.append(attrs["href"])

def get_hyperlinks(url):
    try:
        with urllib.request.urlopen(url) as response:
            if not response.info().get('Content-Type').startswith("text/html"):
                return []
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error getting hyperlinks: {str(e)}")
        return []

    parser = HyperlinkParser()
    parser.feed(html)
    return parser.hyperlinks

def get_domain_hyperlinks(local_domain, url):
    clean_links = []
    for link in set(get_hyperlinks(url)):
        clean_link = None

        if re.search(HTTP_URL_PATTERN, link):
            url_obj = urlparse(link)
            if url_obj.netloc == local_domain:
                clean_link = link
        else:
            if link.startswith("/"):
                link = link[1:]
            elif link.startswith("#") or link.startswith("mailto:"):
                continue
            clean_link = "https://" + local_domain + "/" + link

        if clean_link is not None:
            if clean_link.endswith("/"):
                clean_link = clean_link[:-1]
            clean_links.append(clean_link)

    return list(set(clean_links))

def crawl(url, max_pages=50, max_depth=3):
    """
    Crawl the website with limits on pages and depth
    
    Args:
        url (str): Starting URL to crawl
        max_pages (int): Maximum number of pages to crawl
        max_depth (int): Maximum depth of crawling from start URL
        
    Returns:
        str: The domain name of the crawled website
    """
    local_domain = urlparse(url).netloc
    queue = deque([(url, 0)])  # (url, depth) pairs
    seen = set([url])
    processed_pages = 0

    # Create necessary directories
    os.makedirs("text", exist_ok=True)
    os.makedirs(f"text/{local_domain}", exist_ok=True)
    os.makedirs("processed", exist_ok=True)

    print(f"\nStarting crawl of {local_domain}")
    print(f"Maximum pages to crawl: {max_pages}")
    print(f"Maximum depth: {max_depth}\n")

    while queue and processed_pages < max_pages:
        url, depth = queue.pop()
        
        if depth >= max_depth:
            continue

        print(f"Crawling: {url}")
        print(f"Page {processed_pages + 1} of {max_pages} (Depth: {depth})")

        try:
            # Get the page content
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()

            # Skip if JavaScript is required
            if "You need to enable JavaScript to run this app." in text:
                print(f"JavaScript required for: {url}")
                continue

            # Create filename from URL
            filename = url[8:].replace("/", "_")
            if len(filename) > 100:  # Limit filename length
                filename = filename[:100]

            # Save the content
            file_path = f'text/{local_domain}/{filename}.txt'
            with open(file_path, "w", encoding='utf-8') as f:
                f.write(text)

            processed_pages += 1
            print(f"Saved content to: {file_path}")

            # Check if we've reached the page limit
            if processed_pages >= max_pages:
                print(f"\nReached maximum pages limit ({max_pages})")
                break

            # Get new URLs to process
            new_links = get_domain_hyperlinks(local_domain, url)
            print(f"Found {len(new_links)} new links")

            # Add new URLs to the queue
            for link in new_links:
                if link not in seen:
                    seen.add(link)
                    queue.append((link, depth + 1))

            # Optional: Add a small delay to be nice to the server
            time.sleep(0.5)

        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            continue

    print(f"\nCrawling completed:")
    print(f"Domain: {local_domain}")
    print(f"Total pages processed: {processed_pages}")
    print(f"Remaining URLs in queue: {len(queue)}")
    
    return local_domain
"""
if __name__ == "__main__":
    # Example usage
    test_url = "https://help.slack.com/hc/en-us/articles"
    domain = crawl(test_url, max_pages=50, max_depth=3)
"""
"""
# In you want to iterate through all pages, use below script
import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse
import os

# Regex pattern to match a URL
HTTP_URL_PATTERN = r'^http[s]*://.+'

class HyperlinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hyperlinks = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.hyperlinks.append(attrs["href"])

def get_hyperlinks(url):
    try:
        with urllib.request.urlopen(url) as response:
            if not response.info().get('Content-Type').startswith("text/html"):
                return []
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error getting hyperlinks: {str(e)}")
        return []

    parser = HyperlinkParser()
    parser.feed(html)
    return parser.hyperlinks

def get_domain_hyperlinks(local_domain, url):
    clean_links = []
    for link in set(get_hyperlinks(url)):
        clean_link = None

        if re.search(HTTP_URL_PATTERN, link):
            url_obj = urlparse(link)
            if url_obj.netloc == local_domain:
                clean_link = link
        else:
            if link.startswith("/"):
                link = link[1:]
            elif link.startswith("#") or link.startswith("mailto:"):
                continue
            clean_link = "https://" + local_domain + "/" + link

        if clean_link is not None:
            if clean_link.endswith("/"):
                clean_link = clean_link[:-1]
            clean_links.append(clean_link)

    return list(set(clean_links))

def crawl(url):
    local_domain = urlparse(url).netloc
    queue = deque([url])
    seen = set([url])

    if not os.path.exists("text/"):
        os.mkdir("text/")

    if not os.path.exists("text/"+local_domain+"/"):
        os.mkdir("text/" + local_domain + "/")

    if not os.path.exists("processed"):
        os.mkdir("processed")

    while queue:
        url = queue.pop()
        print(f"Crawling: {url}")

        try:
            with open('text/'+local_domain+'/'+url[8:].replace("/", "_") + ".txt", "w", encoding='utf-8') as f:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text()

                if "You need to enable JavaScript to run this app." in text:
                    print(f"JavaScript required for: {url}")
                    continue

                f.write(text)

            for link in get_domain_hyperlinks(local_domain, url):
                if link not in seen:
                    queue.append(link)
                    seen.add(link)
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            continue

    return local_domain

"""