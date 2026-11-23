# Maestro – Local AI Knowledge Assistant

Maestro is a locally running AI-powered chatbot built with Python, Ollama, and Qwen3. It supports normal conversations, persistent chat history, session management, and Retrieval-Augmented Generation (RAG) to answer questions using information from uploaded PDF documents.

The goal of Maestro is to provide a personal AI assistant that can answer questions using local documents while keeping conversation data stored locally.

## Features

### 1. AI-powered conversations
- Uses Qwen3 8B through Ollama.
- Generates responses using a streaming approach.
- Maintains conversation context across messages.

### 2. Persistent conversation memory
- Uses MongoDB to store conversation messages.
- Maintains separate chat sessions.
- Allows users to create, switch, view, and clear sessions.
- Reloads previous conversation history.

### 3. Retrieval-Augmented Generation (RAG)
- Extracts text from PDF documents using PyPDF.
- Splits extracted text into overlapping chunks.
- Generates vector embeddings using `nomic-embed-text`.
- Stores embeddings persistently in ChromaDB.
- Uses cosine-distance-based similarity search to retrieve relevant document chunks.
- Supplies retrieved context to Qwen3 when answering document-related questions.
- Applies a relevance threshold to reject queries when retrieved chunks do not meet the configured similarity criterion.

### 4. Command-line interface

| Command | Description |
|---|---|
| `/ask <question>` | Ask a question using document context |
| `/history` | View current conversation history |
| `/new <title>` | Create a new chat session |
| `/sessions` | List available sessions |
| `/switch <session_id>` | Switch to another session |
| `/clear` | Clear current session history |
| `exit` / `quit` | Exit Maestro |

## Tech Stack

- **Language:** Python
- **LLM:** Qwen3 8B
- **LLM Runtime:** Ollama
- **Embedding Model:** nomic-embed-text
- **Vector Database:** ChromaDB
- **Database:** MongoDB
- **PDF Processing:** PyPDF
- **Retrieval:** Cosine similarity search

## Project Structure

```text
Maestro/
│
├── main.py              # Main chatbot application
├── llm.py               # Ollama response generation
├── memory.py            # MongoDB conversation management
├── config.py            # Application configuration
├── prompts.py           # System instructions
├── embeddings.py        # PDF processing and embedding storage
├── rag.py               # Document retrieval and context generation
├── test_rag.py          # RAG retrieval testing
│
├── knowledge/
│   ├── lecturenotes.pdf # Knowledge source PDF
│   └── chroma_db/       # Persistent vector database
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.10+
- Ollama
- MongoDB running locally
- Git

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd chatbot
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the required Ollama models

```bash
ollama pull qwen3:8b
ollama pull nomic-embed-text
```

Ensure Ollama is running before starting the application.

### 4. Configure the knowledge document

Place your PDF inside the `knowledge/` directory and configure its path in `embeddings.py`.

### 5. Generate and store embeddings

Run this once when setting up or updating the knowledge document:

```bash
python embeddings.py
```

This extracts the PDF text, creates chunks, generates embeddings, and stores them in ChromaDB.

### 6. Start Maestro

Ensure MongoDB is running locally, then execute:

```bash
python main.py
```

## How RAG Works

```text
             PDF Document
                   |
                   v
             Text Extraction
                   |
                   v
              Text Chunking
                   |
                   v
          Embedding Generation
             (nomic-embed-text)
                   |
                   v
              ChromaDB
                   |
                   |
User Question ---> Query Embedding
                   |
                   v
          Similarity Retrieval
                   |
                   v
          Relevance Threshold
                   |
             Relevant Chunks
                   |
                   v
          Context + User Query
                   |
                   v
                Qwen3
                   |
                   v
             Generated Answer
```

## Future Improvements

- Support multiple PDF documents.
- Improve retrieval relevance and query validation.
- Add a graphical user interface.
- Improve document citation and source tracking.
- Add automated testing and more robust error handling.

## Project Status

The core chatbot, MongoDB-based conversation management, and PDF-based RAG pipeline have been implemented. Further improvements will focus on retrieval reliability, testing, and user experience.
```

