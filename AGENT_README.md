# VectorDB Agent - API Client

A Python agent/client for communicating with the Vector Database Storage API. This agent provides convenient methods to fetch, search, and post information to/from the database.

## Features

- ✅ **Full CRUD Operations** - Create, Read, Update, Delete documents
- ✅ **Semantic Search** - Natural language queries using AI embeddings
- ✅ **Bulk Operations** - Add multiple documents at once
- ✅ **Metadata Filtering** - Search with metadata constraints
- ✅ **Question Answering** - Simple ask() method for direct answers
- ✅ **File Import** - Load documents from JSON files
- ✅ **Type-Safe** - Uses httpx for robust HTTP communication

## Installation

The agent requires `httpx` which is already installed in the project:

```bash
pip install httpx
```

## Quick Start

```python
from agent import VectorDBAgent

# Create agent (uses http://localhost:8000 by default)
with VectorDBAgent() as agent:
    # Health check
    health = agent.health_check()
    print(f"API Status: {health['status']}")
    
    # Ask a question
    answer = agent.ask("what is my name?")
    print(f"Answer: {answer}")
```

## Usage Examples

### 1. Adding Documents

**Single Document:**
```python
with VectorDBAgent() as agent:
    doc_id = agent.add_document(
        document="I love hiking in the mountains",
        metadata={"category": "hobbies", "type": "outdoor"}
    )
    print(f"Created document: {doc_id}")
```

**Multiple Documents:**
```python
with VectorDBAgent() as agent:
    doc_ids = agent.add_documents(
        documents=[
            "I work as a machine learning engineer",
            "My favorite programming language is Python",
            "I enjoy building AI applications"
        ],
        metadatas=[
            {"category": "work", "type": "role"},
            {"category": "tech", "type": "language"},
            {"category": "work", "type": "interests"}
        ]
    )
    print(f"Created {len(doc_ids)} documents")
```

**From JSON File:**
```python
with VectorDBAgent() as agent:
    doc_ids = agent.add_from_file("BulkInsert.json")
    print(f"Imported {len(doc_ids)} documents")
```

### 2. Searching Information

**Basic Search:**
```python
with VectorDBAgent() as agent:
    results = agent.search("what is my name?", n_results=3)
    
    for i, doc in enumerate(results["documents"], 1):
        print(f"{i}. {doc}")
        print(f"   Score: {results['distances'][i-1]}")
```

**Search with Metadata Filter:**
```python
with VectorDBAgent() as agent:
    results = agent.search(
        query="personal information",
        n_results=5,
        where={"category": "personal-info"}
    )
    
    # Pretty print results
    agent.print_search_results(results)
```

**Simple Question Answering:**
```python
with VectorDBAgent() as agent:
    # Returns just the most relevant document text
    answer = agent.ask("where do I live?")
    print(answer)  # "I live in Coimbatore"
```

### 3. Retrieving Documents

**Get Specific Document:**
```python
with VectorDBAgent() as agent:
    doc = agent.get_document("abc-123")
    print(f"Document: {doc['document']}")
    print(f"Metadata: {doc['metadata']}")
```

**Get All Documents:**
```python
with VectorDBAgent() as agent:
    all_docs = agent.get_all_documents(limit=10)
    
    for doc in all_docs:
        print(f"- {doc['document']}")
```

**Find by Metadata:**
```python
with VectorDBAgent() as agent:
    docs = agent.find_by_metadata(category="personal-info")
    
    for doc in docs:
        print(f"- {doc['document']}")
```

### 4. Updating Documents

```python
with VectorDBAgent() as agent:
    # Update metadata
    agent.update_document(
        doc_id="abc-123",
        metadata={"category": "updated", "verified": True}
    )
    
    # Update content
    agent.update_document(
        doc_id="abc-123",
        document="New content for this document"
    )
```

### 5. Deleting Documents

**Delete Single Document:**
```python
with VectorDBAgent() as agent:
    success = agent.delete_document("abc-123")
    print(f"Deleted: {success}")
```

**Delete All Documents:**
```python
with VectorDBAgent() as agent:
    # WARNING: This deletes everything!
    success = agent.reset_collection()
```

### 6. Collection Statistics

```python
with VectorDBAgent() as agent:
    stats = agent.get_stats()
    print(f"Total documents: {stats['total_documents']}")
```

## Agent Methods Reference

### Connection Methods
- `__init__(base_url, timeout)` - Initialize agent
- `health_check()` - Check API status
- `get_stats()` - Get collection statistics
- `close()` - Close HTTP client

### Create Operations
- `add_document(document, metadata, doc_id)` - Add single document
- `add_documents(documents, metadatas, ids)` - Add multiple documents
- `add_from_dict(data)` - Add from dictionary
- `add_from_file(filepath)` - Add from JSON file

### Read Operations
- `get_document(doc_id)` - Get specific document
- `get_all_documents(limit)` - Get all documents
- `search(query, n_results, where)` - Semantic search
- `ask(question, n_results)` - Simple Q&A interface
- `find_by_metadata(category, **filters)` - Filter by metadata

### Update Operations
- `update_document(doc_id, document, metadata)` - Update document

### Delete Operations
- `delete_document(doc_id)` - Delete single document
- `reset_collection()` - Delete all documents

### Utility Methods
- `print_search_results(results)` - Pretty print search results

## Running the Examples

The project includes comprehensive examples:

```bash
# Run all examples
python agent_examples.py

# Run specific example
python agent_examples.py 1  # Basic CRUD
python agent_examples.py 2  # Bulk operations
python agent_examples.py 3  # Semantic search
python agent_examples.py 4  # File operations
python agent_examples.py 5  # Metadata filtering
python agent_examples.py 6  # Question answering
python agent_examples.py 7  # Interactive mode
```

## Interactive Mode

Run the interactive question-answering mode:

```bash
python agent_examples.py 7
```

Then ask questions:
```
❓ You: what is my name?
💡 Answer: I am Rameshkartik, a software engineer...

❓ You: where do I live?
💡 Answer: I live in Coimbatore

❓ You: quit
```

## Configuration

The agent connects to `http://localhost:8000` by default. To use a different server:

```python
agent = VectorDBAgent(
    base_url="http://your-server:8000",
    timeout=30.0  # Request timeout in seconds
)
```

## Error Handling

The agent uses httpx which raises exceptions for HTTP errors:

```python
import httpx
from agent import VectorDBAgent

with VectorDBAgent() as agent:
    try:
        result = agent.search("test query")
    except httpx.ConnectError:
        print("Cannot connect to API server")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code}")
```

## Context Manager Support

The agent supports Python's context manager protocol:

```python
# Automatically closes the HTTP client
with VectorDBAgent() as agent:
    results = agent.search("query")
    # ... do work ...
# Client closed automatically
```

Or manually:

```python
agent = VectorDBAgent()
try:
    results = agent.search("query")
finally:
    agent.close()
```

## Complete Example

```python
from agent import VectorDBAgent

# Example workflow
with VectorDBAgent() as agent:
    # 1. Check connection
    health = agent.health_check()
    print(f"API Status: {health['status']}")
    
    # 2. Add personal information
    doc_id = agent.add_document(
        document="I love playing chess on weekends",
        metadata={"category": "hobbies", "activity": "chess"}
    )
    
    # 3. Search for it
    results = agent.search("what are my hobbies?", n_results=3)
    print(f"Found: {results['documents'][0]}")
    
    # 4. Update the document
    agent.update_document(
        doc_id,
        metadata={"category": "hobbies", "activity": "chess", "verified": True}
    )
    
    # 5. Get statistics
    stats = agent.get_stats()
    print(f"Total documents: {stats['total_documents']}")
```

## API Server Requirement

The agent requires the API server to be running:

```bash
# Start the server in another terminal
python api.py

# Then use the agent
python test_agent.py
```

## See Also

- [README.md](README.md) - Main project documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [api.py](api.py) - API server implementation
- [storage.py](storage.py) - Storage layer
