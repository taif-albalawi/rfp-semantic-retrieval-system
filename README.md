# RFP Semantic Retrieval System

An AI-powered Retrieval-Augmented Generation (RAG) system for semantic search and intelligent question answering over Request for Proposal (RFP) documents.

---

## Overview

RFP Semantic Retrieval System helps users quickly retrieve relevant information from large collections of RFP documents using semantic search and Large Language Models (LLMs).

The system supports document ingestion, semantic retrieval, question answering with source references, and a basic Bid / No-Bid recommendation module.

---

## Features

- Semantic search using FAISS
- Retrieval-Augmented Generation (RAG)
- Question Answering over RFP documents
- Bid / No-Bid recommendation
- Source document retrieval
- FastAPI backend
- Streamlit frontend
- Evaluation pipeline

---

## Supported File Types

- PDF
- DOCX
- XLSX
- PPTX

---

## Tech Stack

- Python
- LangChain
- OpenAI GPT-4o-mini
- HuggingFace Embeddings
- FAISS
- FastAPI
- Streamlit
- Pandas

---

## Project Structure

```text
ai-rag-project/
│
├── frontend/
│   └── app.py
│
├── bid_decision.py
├── chunking.py
├── embedder.py
├── evaluate.py
├── ingestion.py
├── ingestion_faiss.py
├── llm.py
├── main.py
├── prompt.py
├── rag_chain.py
├── requirements.txt
├── retriever.py
├── test_queries.py
├── vectorstore.py
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/taif-albalawi/rfp-semantic-retrieval-system.git
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configure API Key

Set your OpenAI API key before running the project.

Example:

```bash
export OPENAI_API_KEY="YOUR_API_KEY"
```

---

## Build the Vector Database

Place your own RFP documents inside the `data/` folder, then run:

```bash
python3 ingestion_faiss.py
```

This will create the local FAISS index.

> **Note:** The original RFP dataset is **not included** in this repository because it contains confidential documents.

---

## Run the Backend

```bash
uvicorn main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

---

## Run the Frontend

Open another terminal:

```bash
streamlit run frontend/app.py
```

---

## API Endpoints

### Ask Questions

```
POST /ask
```

Returns:
- Generated answer
- Source documents

### Bid / No-Bid

```
POST /bid
```

Returns:
- Bid
- No-Bid
- Maybe

with reasoning based on the retrieved documents.

---

## Future Improvements

- Advanced document filtering
- Better ranking models
- Confidence scoring
- Authentication
- Cloud deployment
- Multi-user support

---

## Authors

- **Taif Albalawi**

Developed as part of the **Saudi Digital Academy (SDA) AI Engineering Bootcamp**.