


import argparse
import os
import pandas as pd
import logging
from urllib.parse import urlparse
from langchain_community.document_loaders import DataFrameLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain_google_genai import HarmBlockThreshold, HarmCategory
#from crawler import crawl, process_text_files
import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse
import os
import time
import os
import pandas as pd
import csv

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

def remove_newlines(text):
    if text is None:
        return ""
    text = str(text)
    text = text.replace('\n', ' ')
    text = text.replace('\\n', ' ')
    return ' '.join(text.split())

def process_text_files(domain):
    os.makedirs(f"text/{domain}", exist_ok=True)
    os.makedirs("processed", exist_ok=True)
    
    texts = []
    text_dir = f"text/{domain}/"
    
    for file in os.listdir(text_dir):
        file_path = os.path.join(text_dir, file)
        if os.path.isfile(file_path) and not file.startswith('.'):
            try:
                with open(file_path, "r", encoding='utf-8') as f:
                    text = f.read()
                    processed_name = os.path.splitext(file)[0]
                    texts.append((processed_name, text))
            except Exception as e:
                print(f"Error processing file {file}: {str(e)}")
    
    df = pd.DataFrame(texts, columns=['fname', 'text'])
    df['text'] = df['text'].apply(remove_newlines)
    
    output_path = 'processed/scraped.csv'
    try:
        df.to_csv(output_path, 
                 index=False,
                 escapechar='\\',
                 doublequote=True,
                 encoding='utf-8',
                 quoting=csv.QUOTE_ALL)
        print(f"Processed {len(texts)} files and saved to {output_path}")
    except Exception as e:
        print(f"Error saving CSV: {str(e)}")
        df['text'] = df['text'].replace(r'[\x00-\x1F\x7F-\x9F]', '', regex=True)
        df.to_csv(output_path,
                 index=False,
                 encoding='utf-8',
                 escapechar='\\')
    
    return df


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QAAgent:
    def __init__(self, google_api_key):
        """Initialize the QA Agent with Google API key."""
        os.environ["GOOGLE_API_KEY"] = google_api_key
        self.vectorstore = None
        self.rag_chain = None
        self.domain = None

    def initialize_system(self, url):
        """Initialize the system with a URL to crawl."""
        try:
            # Crawl the website
            logger.info(f"Starting crawl of {url}")
            self.domain = crawl(url, max_pages=50, max_depth=3)
            
            # Process the crawled text files
            logger.info("Processing crawled content...")
            df = process_text_files(self.domain)
            
            # Initialize the QA system
            logger.info("Initializing QA system...")
            return self.initialize_vectorstore(df)
            
        except Exception as e:
            logger.error(f"Error initializing system: {str(e)}")
            return False

    def initialize_vectorstore(self, df):
        """Initialize the vector store with processed documents."""
        try:
            loader = DataFrameLoader(df, page_content_column="text")
            documents = loader.load()
            
            gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                safety_settings={
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
            )
            
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=gemini_embeddings,
                persist_directory="chroma_db"
            )
            
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": 10})
            
            template = """You are an assistant for question-answering tasks.
            Use the following context to answer the question.
            If you don't know the answer, just say that you don't know.
            Keep the answer concise.
            Add the metadata or source of the document where you get the answer.
            
            Question: {question} 
            Context: {context} 
            Answer:"""
            
            prompt = PromptTemplate.from_template(template)
            
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)
            
            self.rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error initializing vectorstore: {str(e)}")
            return False

    def get_answer(self, question):
        """Get answer for a question."""
        if self.rag_chain is None:
            return "System not initialized. Please initialize first."
        try:
            return self.rag_chain.invoke(question)
        except Exception as e:
            return f"Error generating answer: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description='Documentation QA Agent')
    parser.add_argument('--url', required=True, help='Documentation website URL to crawl')
    parser.add_argument('--api-key', required=True, help='Google API Key')
    args = parser.parse_args()

    # Initialize the agent
    agent = QAAgent(args.api_key)
    
    # Initialize the system with the provided URL
    logger.info("Initializing system...")
    if agent.initialize_system(args.url):
        logger.info("System initialized successfully!")
    else:
        logger.error("Failed to initialize system")
        return

    # Start interactive loop
    print("\nQA Agent ready! Type 'quit' to exit.\n")
    while True:
        try:
            question = input("> ").strip()
            
            if question.lower() == 'quit':
                break
                
            if question:
                answer = agent.get_answer(question)
                print(f"\n{answer}\n")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()