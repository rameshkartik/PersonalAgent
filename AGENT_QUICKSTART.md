# VectorDB Agent - Quick Reference

## What is the Agent?

The VectorDB Agent is a Python client that communicates with your Vector Database API to:
- **POST** information (add documents)
- **FETCH** information (retrieve documents)
- **SEARCH** information (semantic queries)

## Installation

Already included in your project! Just make sure the API server is running:

```bash
python api.py
```

## Basic Usage

### 1. Import and Connect

```python
from agent import VectorDBAgent

# Create agent (connects to http://localhost:8000)
with VectorDBAgent() as agent:
    # Your code here
    pass
```

### 2. Add Information (POST)

```python
with VectorDBAgent() as agent:
    # Add single document
    doc_id = agent.add_document(
        document="I graduated from MIT in 2020",
        metadata={"category": "education", "year": "2020"}
    )
    
    # Add multiple documents
    ids = agent.add_documents(
        documents=[
            "I love playing guitar",
            "My favorite food is pizza"
        ],
        metadatas=[
            {"category": "hobbies"},
            {"category": "preferences"}
        ]
    )
    
    # Load from file
    ids = agent.add_from_file("BulkInsert.json")
```

### 3. Search Information (SEARCH)

```python
with VectorDBAgent() as agent:
    # Semantic search
    results = agent.search("what are my hobbies?", n_results=5)
    
    # With metadata filter
    results = agent.search(
        "information about me",
        where={"category": "personal-info"}
    )
    
    # Simple question answering
    answer = agent.ask("where do I live?")
    print(answer)  # "I live in Coimbatore"
```

### 4. Fetch Information (FETCH)

```python
with VectorDBAgent() as agent:
    # Get specific document by ID
    doc = agent.get_document("abc-123")
    print(doc["document"])
    
    # Get all documents
    all_docs = agent.get_all_documents(limit=10)
    
    # Find by metadata
    docs = agent.find_by_metadata(category="work")
    
    # Get statistics
    stats = agent.get_stats()
    print(f"Total: {stats['total_documents']}")
```

### 5. Update & Delete

```python
with VectorDBAgent() as agent:
    # Update document
    agent.update_document(
        "abc-123",
        document="Updated content",
        metadata={"verified": True}
    )
    
    # Delete document
    agent.delete_document("abc-123")
```

## Running Tests

```bash
# Simple test
python test_agent.py

# Basic demo
python agent.py

# All examples
python agent_examples.py 6
```

## Common Use Cases

### Personal Information Storage

```python
with VectorDBAgent() as agent:
    # Store information
    agent.add_document("My favorite color is blue", {"category": "preferences"})
    agent.add_document("I speak English and Spanish", {"category": "languages"})
    
    # Query it later
    answer = agent.ask("what languages do I speak?")
    # "I speak English and Spanish"
```

### Work/Project Information

```python
with VectorDBAgent() as agent:
    # Add project info
    agent.add_documents(
        documents=[
            "ProjectX uses React and Node.js",
            "ProjectX deadline is March 2026",
            "ProjectX team has 5 members"
        ],
        metadatas=[
            {"project": "ProjectX", "type": "tech-stack"},
            {"project": "ProjectX", "type": "timeline"},
            {"project": "ProjectX", "type": "team"}
        ]
    )
    
    # Search project info
    results = agent.search(
        "ProjectX technologies",
        where={"project": "ProjectX"}
    )
```

### Knowledge Base

```python
with VectorDBAgent() as agent:
    # Add knowledge
    agent.add_document(
        "Python list comprehensions are written as [x for x in iterable]",
        metadata={"language": "Python", "topic": "syntax"}
    )
    
    # Query knowledge
    answer = agent.ask("how to write list comprehensions?")
```

## API Methods Summary

| Method | Description | Example |
|--------|-------------|---------|
| `add_document()` | Add single document | `id = agent.add_document("text", {...})` |
| `add_documents()` | Add multiple documents | `ids = agent.add_documents([...], [...])` |
| `search()` | Semantic search | `results = agent.search("query", 5)` |
| `ask()` | Quick Q&A | `answer = agent.ask("question?")` |
| `get_document()` | Get by ID | `doc = agent.get_document("id")` |
| `get_all_documents()` | Get all docs | `docs = agent.get_all_documents()` |
| `update_document()` | Update doc | `agent.update_document("id", "new")` |
| `delete_document()` | Delete doc | `agent.delete_document("id")` |
| `get_stats()` | Get stats | `stats = agent.get_stats()` |

## Full Example

```python
from agent import VectorDBAgent

# Complete workflow
with VectorDBAgent() as agent:
    # 1. Add your information
    print("Adding information...")
    agent.add_documents(
        documents=[
            "I am a software engineer",
            "I live in San Francisco",
            "I have 5 years of Python experience"
        ],
        metadatas=[
            {"category": "work"},
            {"category": "location"},
            {"category": "skills"}
        ]
    )
    
    # 2. Search for information
    print("\nSearching...")
    results = agent.search("tell me about myself", n_results=3)
    agent.print_search_results(results)
    
    # 3. Ask questions
    print("\nAsking questions...")
    questions = [
        "what do I do?",
        "where do I live?",
        "what are my skills?"
    ]
    
    for q in questions:
        answer = agent.ask(q)
        print(f"Q: {q}")
        print(f"A: {answer}\n")
```

## Troubleshooting

**Cannot connect to API:**
```bash
# Make sure server is running
python api.py
```

**httpx not installed:**
```bash
pip install httpx
```

**Need to change server URL:**
```python
agent = VectorDBAgent(base_url="http://your-server:8000")
```

## Next Steps

1. ✅ **Your agent is ready to use!**
2. 📖 Read [AGENT_README.md](AGENT_README.md) for detailed documentation
3. 🔍 Try [agent_examples.py](agent_examples.py) for more examples
4. 🚀 Build your own applications using the agent

## Support

- Main README: [README.md](README.md)
- API Documentation: http://localhost:8000/docs
- Example Code: [agent_examples.py](agent_examples.py)
