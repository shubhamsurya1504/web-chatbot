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
