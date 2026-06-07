# FAISS Knowledge Base Integration Guide

## Overview

This project uses FAISS (Facebook AI Similarity Search) for semantic search on the knowledge base. FAISS provides fast similarity search using vector embeddings, allowing the agent to find relevant documents based on semantic meaning rather than just keyword matching.

## Architecture

### Components

1. **FAISSKBService** (`src/services/faiss_kb.py`)
   - Manages FAISS index creation and search
   - Handles document loading and embedding
   - Provides fallback search when FAISS is unavailable

2. **Context Analysis Node** (`src/nodes/context_analysis.py`)
   - Uses FAISS to search the knowledge base
   - Passes relevant documents to response generation

3. **Sample Documents** (`data/kb_documents.json`)
   - 10 comprehensive customer support documents
   - Covers: returns, shipping, billing, support, account, warranty, quality, sales, subscription, products

4. **FAISS Index** (`data/faiss_index/`)
   - Auto-created on first run
   - Stores vector embeddings of all documents
   - Enables fast semantic similarity search

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Key packages:
- `faiss-cpu>=1.7.4` — Vector similarity search
- `langchain-community>=0.1.0` — FAISS integration
- `langchain-openai` — Embeddings generation

### 2. Initialize FAISS Index

Before running the application, initialize the FAISS index:

```bash
python scripts/initialize_faiss.py
```

This creates the FAISS index from the sample documents using OpenAI embeddings.

## Usage

### Automatic (in Workflow)

The FAISS search happens automatically in the workflow:
1. Email arrives
2. Intent classified
3. **FAISS searches for relevant documents**
4. Response generated using context
5. Response sent to customer

### Manual Testing

Test FAISS search with sample queries:

```bash
python scripts/test_faiss.py
```

Example queries tested:
- "How do I return an item?"
- "What is your shipping policy?"
- "I need help with technical issues"
- "Payment methods and billing"

### API Usage

When processing an email via the API, FAISS automatically searches and retrieves relevant documents:

```bash
curl -X POST "http://localhost:8000/api/email" \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "customer@example.com",
    "recipient": "support@example.com",
    "subject": "Can I return my order?",
    "body": "I received the wrong size and want to return it. How does that work?"
  }'
```

Response will include documents about return policy retrieved via FAISS.

## Adding New Documents

To add documents to the knowledge base:

```python
from src.services.faiss_kb import get_faiss_kb_service

faiss_kb = get_faiss_kb_service()

new_doc = {
    "id": "custom_policy",
    "title": "Custom Policy Title",
    "content": "Detailed policy content here...",
    "category": "policy"
}

faiss_kb.add_document(new_doc)
```

This:
1. Adds the document to `data/kb_documents.json`
2. Recreates the FAISS index with embeddings
3. Makes the document immediately searchable

## How It Works

### Embedding Generation

1. **Documents** are loaded from `data/kb_documents.json`
2. **OpenAI Embeddings** convert text to vectors (1536-dimensional)
3. **FAISS Index** stores vectors for fast similarity search

### Semantic Search

When a query comes in:
1. Query is converted to an embedding
2. FAISS finds the k-nearest neighbors in vector space
3. Documents with highest similarity scores are returned
4. Results are ranked by relevance score (0-1, where 1 is perfect match)

### Fallback Search

If FAISS is unavailable or has errors:
- Simple keyword search is used on title, content, and category
- Ensures the system continues working gracefully

## Performance

- **Index Creation**: ~5-10 seconds for 10 documents
- **Search Time**: ~10-50ms for semantic search
- **Memory**: ~50MB for small knowledge bases

## Customization

### Change Number of Results

In `src/nodes/context_analysis.py`:

```python
results = faiss_kb_service.search(query, top_k=5)  # Get top 5 instead of 3
```

### Change Embedding Model

In `src/services/faiss_kb.py`:

```python
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings

# Use HuggingFace instead of OpenAI
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
```

### Use GPU Version

Install FAISS with GPU support:

```bash
pip install faiss-gpu
```

Then update import in `faiss_kb.py`:
- No code changes needed, FAISS automatically uses GPU if available

## Troubleshooting

### "ModuleNotFoundError: No module named 'faiss'"

Solution:
```bash
pip install faiss-cpu
```

### FAISS index not found

Solution:
```bash
python scripts/initialize_faiss.py
```

### Slow search performance

- Use GPU version: `pip install faiss-gpu`
- Reduce `top_k` parameter
- Use smaller embedding model

### Poor search results

- Check document quality in `data/kb_documents.json`
- Increase number of documents
- Use more specific document titles and content
- Test with `python scripts/test_faiss.py`

## Monitoring

FAISS operations are logged:

```
INFO: Found 3 relevant documents via FAISS semantic search
DEBUG: - Returns and Refunds Policy (score: 0.8234)
DEBUG: - Shipping and Delivery (score: 0.6123)
DEBUG: - Product Warranty (score: 0.5892)
```

Monitor these logs to understand search quality and relevance scores.
