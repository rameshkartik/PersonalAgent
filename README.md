# Vector DB Storage Layer with External API

A complete storage solution using Qdrant vector database with a FastAPI-based external REST API.

## Features

- **Vector Storage**: Store and retrieve documents using Qdrant's vector database
- **REST API**: Full-featured external API for managing your data
- **Semantic Search**: Query documents by similarity using AI embeddings
- **Metadata Support**: Attach custom metadata to documents
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality
- **Bulk Operations**: Add multiple documents at once
- **Python 3.14 Compatible**: Works with the latest Python version

## Project Structure

```
PerAgent/
├── api.py              # FastAPI application
├── storage.py          # Qdrant vector DB storage layer
├── models.py           # Pydantic models for validation
├── config.py           # Configuration management
├── download_model.py   # Pre-download embedding model
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Setup

### 1. Create a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Download the AI embedding model (one-time setup)

```powershell
python download_model.py
```

This downloads the `all-MiniLM-L6-v2` model (~90MB). This is a one-time download that enables semantic search.

### 4. Configure environment (optional)

Copy `.env.example` to `.env` and customize if needed:

```powershell
Copy-Item .env.example .env
```

### 5. Run the API server

```powershell
python api.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /` - Health check endpoint

### Statistics
- `GET /stats` - Get collection statistics

### Document Management
- `POST /documents` - Create a new document
- `POST /documents/bulk` - Create multiple documents
- `GET /documents/{doc_id}` - Get a document by ID
- `GET /documents` - Get all documents
- `PUT /documents/{doc_id}` - Update a document
- `DELETE /documents/{doc_id}` - Delete a document

### Search
- `POST /query` - Query documents by similarity

### Management
- `DELETE /reset` - Reset collection (delete all documents)

## Usage Examples

### Using curl

#### Create a document
```bash
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "document": "This is my personal information about my favorite color: blue",
    "metadata": {"category": "preferences", "type": "color"}
  }'
```

#### Query documents
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "what is my favorite color?",
    "n_results": 3
  }'
```

#### Get all documents
```bash
curl -X GET "http://localhost:8000/documents"
```

### Using Python

```python
import httpx

# Create a document
response = httpx.post(
    "http://localhost:8000/documents",
    json={
        "document": "I live in New York City",
        "metadata": {"category": "location"}
    }
)
print(response.json())

# Query documents
response = httpx.post(
    "http://localhost:8000/query",
    json={
        "query_text": "where do I live?",
        "n_results": 5
    }
)
print(response.json())
```

## Storage Layer Usage

You can also use the storage layer directly in your Python code:

```python
from storage import get_storage

# Get storage instance
storage = get_storage()

# Add a document
doc_id = storage.add_document(
    document="My birthday is January 15th",
    metadata={"category": "personal", "type": "birthday"}
)

# Query documents
results = storage.query_documents(
    query_text="when is my birthday?",
    n_results=3
)

# Get a specific document
doc = storage.get_document(doc_id)

# Update a document
storage.update_document(
    doc_id=doc_id,
    metadata={"category": "personal", "type": "birthday", "verified": True}
)

# Delete a document
storage.delete_document(doc_id)
```

## Configuration

Edit `.env` file to customize:

- `CHROMA_PERSIST_DIRECTORY`: Directory for ChromaDB data storage
- `CHROMA_COLLECTION_NAME`: Name of the ChromaDB collection
- `API_HOST`: API server host
- `API_PORT`: API server port
- `API_RELOAD`: Enable auto-reload for development

## Data Persistence

All data is persisted to the `vector_data/` directory by default. This directory is created automatically and contains your Qdrant vector database collection data.

## Troubleshooting

### First-time startup is slow
The first time you run the server, it downloads the AI embedding model (~90MB). Run `python download_model.py` separately first to avoid this delay.

## Security Notes

This is a basic implementation. For production use, consider adding:
- Authentication and authorization
- API rate limiting
- Input validation and sanitization
- HTTPS/TLS encryption
- CORS configuration
- Request logging and monitoring

## License

MIT

## RDEData
title : PersonalAgent
description : A Personal Agent to take care of personal day to day work
category : Whitepapers
sdlcStage : plan
personas : ['CTO','Enterprise Architect','AI Developer']
tags : ['AI','Agents']
metadata: { capability: 'Storage Solution', integrationType: 'Semantic Search', scope: 'Multi-Service Deployments' }

