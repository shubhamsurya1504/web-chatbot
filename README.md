<h1 align="center">🔍 Pulse - Help Website Q&A Agent</h1>

<!-- Center-align the logo and set its size -->
<p align="center">
  <img src="https://github.com/user-attachments/assets/fc619cf4-f0ce-4e30-9884-a9a6a6623940" alt="Pulse-WebQA Agent Logo" width="175" height="175"/>
</p>


A powerful documentation QA system that crawls help websites, processes content, and provides accurate answers using RAG (Retrieval-Augmented Generation) with Google's Gemini AI.

### Python Packages For Building QA Agent 
![Static Badge](https://img.shields.io/badge/Python-3.10slim-blue)
![Static Badge](https://img.shields.io/badge/pandas-2.2.3-red)
![Static Badge](https://img.shields.io/badge/langchain_community-0.3.12-yellow)
![Static Badge](https://img.shields.io/badge/langchain_google_vertexai-2.0.9-lightblue)
![Static Badge](https://img.shields.io/badge/langchain_google_genai-2.0.7-green)
![Static Badge](https://img.shields.io/badge/chromadb-0.5.23-purple)
![Static Badge](https://img.shields.io/badge/gradio-5.9.1-yellow)


## Table of Contents

1. Flow Diagram / Architecture
2. Storage Structure
3. Features
4. Installation
5. Usage
6. Contributing

## Flow Diagram / Architecture

<p align="center">
<img src="https://github.com/user-attachments/assets/ffd28e21-b531-4d8e-b36b-38e097cc0c44"/>
</p>

## Storage Structure

```
Pulse-WebQA_Agent/
├──notebooks
├── text/                    # Raw crawled content
│   └── domain.com/
│       ├── page1.txt
│       └── page2.txt
├── processed/              # Processed content
│   └── scraped.csv
├── chroma_db/             # Vector database
│   ├── index/
│   └── embeddings/
└── src
    ├── app.py
    ├── crawler.py
    ├── processor.py
    └── qa_system.py
├── requirements.txt
├── run.py
├── docker-compose.yml
├── Dockerfile
└── setup.py

```
## Features

### 🌐 Smart Web Crawling

* Configurable depth and page limits
* Intelligent URL filtering
* Progress tracking


### 📑 Content Processing

* Removes irrelevant elements (navigation, footers)
* Preserves document hierarchy
* Handles multiple content types


### 🧠 Advanced RAG System

* Google's Gemini AI integration
* Semantic search capabilities
* Context-aware responses


### 💾 Extensible Storage

* Chromadb vector database
* Supports appending new content
* Efficient retrieval

## Installation
1. Clone the repository:
   
```
git clone https://github.com/rajeshmore1/Pulse-WebQA_Agent.git
cd Pulse-WebQA_Agent
```
2. Create a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```
pip install -r requirements.txt

```
4. Set up environment variables:

```
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```
## Usage

Starting the Application
```
python app.py
```

Running Unit Test
```
python -m unittest test_crawler.py -v
```
## Web Interface

![image](https://github.com/user-attachments/assets/1da9b727-59ba-42bf-a141-14a3f4229950)

## Containerisation

Build the Docker image:

```
docker build -t pulse-qa .
```
Run using Docker Compose:

```
# Create .env file with your API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Start the application
docker-compose up
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Open a pull request
