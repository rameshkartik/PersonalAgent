# Quick Start Guide

## ✅ Issue Resolved!

Your storage layer with vector database is ready to use. Here's what was done:

### Problem
-Python 3.14 is too new for ChromaDB (incompatibility with Pydantic v1)

### Solution
- ✅ Replaced ChromaDB with **Qdrant** (fully Python 3.14 compatible)
- ✅ Added **sentence-transformers** for AI-powered semantic search
- ✅ Installed all dependencies successfully
- ✅ Updated all code and configuration

## 🚀 Start Using It Now

### Step 1: Download the AI model (one-time, ~2-3 minutes)

```powershell
python download_model.py
```

### Step 2: Start the server

```powershell
python api.py
```

### Step 3: Access the API

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📝 Quick Test

Once the server is running, try these in a new terminal:

```powershell
# Add a document
curl http://localhost:8000/documents -Method POST -ContentType "application/json" -Body '{"document": "I love programming in Python", "metadata": {"category": "hobbies"}}'

# Search for similar content
curl http://localhost:8000/query -Method POST -ContentType "application/json" -Body '{"query_text": "what do I enjoy?", "n_results": 3}'
```

Or run the example script:

```powershell
python example.py
```

## 📖 What You Get

- **Semantic Search**: Find documents by meaning, not just keywords
- **REST API**: Easy external access from any application
-**Metadata Filtering**: Organize and filter your data
- **Persistent Storage**: All data saved in `vector_data/` directory
- **Auto-generated API Docs**: Interactive documentation at /docs

## 🔧 Technology Stack

- **Qdrant**: High-performance vector database
- **FastAPI**: Modern web framework for APIs
- **Sentence Transformers**: State-of-the-art text embeddings
- **Python 3.14**: Latest Python version

Enjoy your new storage layer! 🎉
