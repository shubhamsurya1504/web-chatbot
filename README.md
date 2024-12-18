<h1 align="center">🔍 Pulse - Help Website Q&A Agent</h1>

<!-- Center-align the logo and set its size -->
<p align="center">
  <img src="https://github.com/user-attachments/assets/fc619cf4-f0ce-4e30-9884-a9a6a6623940" alt="Deepcure Logo" width="175" height="175"/>
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

1. Architecture
2. Features
3. Installation
4. Usage
5. Technical Details
6. Contributing

## Storage Structure

```
pulse-qa/
├── text/                    # Raw crawled content
│   └── domain.com/
│       ├── page1.txt
│       └── page2.txt
├── processed/              # Processed content
│   └── scraped.csv
├── chroma_db/             # Vector database
│   ├── index/
│   └── embeddings/
├── src
    ├── app.py
    ├── crawler.py
    ├── processor.py
    └── qa_system.py
```
## Features

### 🌐 Smart Web Crawling

* Configurable depth and page limits *Intelligent URL filtering *Progress tracking


### 📑 Content Processing

* Removes irrelevant elements (navigation, footers) * Preserves document hierarchy * Handles multiple content types


### 🧠 Advanced RAG System

* Google's Gemini AI integration * Semantic search capabilities * Context-aware responses


### 💾 Extensible Storage

* Chromadb vector database * Supports appending new content * Efficient retrieval
  
## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Open a pull request
