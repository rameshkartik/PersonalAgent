"""
Example usage of the ChromaDB Storage Layer and API.
This script demonstrates various operations you can perform.
"""
import httpx
import time


# API Base URL
BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def example_api_usage():
    """Demonstrate API usage with httpx."""
    
    print_section("ChromaDB Storage API - Example Usage")
    
    # Health check
    print("1. Health Check")
    response = httpx.get(f"{BASE_URL}/")
    print(f"Status: {response.json()}\n")
    
    # Create a single document
    print("2. Creating a document")
    response = httpx.post(
        f"{BASE_URL}/documents",
        json={
            "document": "My favorite programming language is Python. I love it for data science and web development.",
            "metadata": {"category": "preferences", "type": "programming"}
        }
    )
    doc1_id = response.json()["id"]
    print(f"Created document: {response.json()}\n")
    
    # Create multiple documents
    print("3. Creating multiple documents")
    response = httpx.post(
        f"{BASE_URL}/documents/bulk",
        json={
            "documents": [
                "I was born in San Francisco, California.",
                "My birthday is on March 15th, 1990.",
                "I graduated from Stanford University with a degree in Computer Science.",
                "My favorite hobby is playing guitar and writing music."
            ],
            "metadatas": [
                {"category": "personal", "type": "location"},
                {"category": "personal", "type": "birthday"},
                {"category": "education", "type": "degree"},
                {"category": "hobbies", "type": "music"}
            ]
        }
    )
    print(f"Created {response.json()['count']} documents\n")
    
    # Wait a moment for indexing
    time.sleep(1)
    
    # Get collection stats
    print("4. Getting collection statistics")
    response = httpx.get(f"{BASE_URL}/stats")
    print(f"Stats: {response.json()}\n")
    
    # Query documents
    print("5. Querying documents - 'Where was I born?'")
    response = httpx.post(
        f"{BASE_URL}/query",
        json={
            "query_text": "Where was I born?",
            "n_results": 2
        }
    )
    results = response.json()
    print(f"Found {len(results['documents'])} results:")
    for i, (doc, dist) in enumerate(zip(results['documents'], results['distances'])):
        print(f"  {i+1}. {doc} (distance: {dist:.4f})")
    print()
    
    # Another query
    print("6. Querying documents - 'What do I like to do?'")
    response = httpx.post(
        f"{BASE_URL}/query",
        json={
            "query_text": "What do I like to do for fun?",
            "n_results": 2
        }
    )
    results = response.json()
    print(f"Found {len(results['documents'])} results:")
    for i, (doc, dist) in enumerate(zip(results['documents'], results['distances'])):
        print(f"  {i+1}. {doc} (distance: {dist:.4f})")
    print()
    
    # Get a specific document
    print("7. Getting a specific document by ID")
    response = httpx.get(f"{BASE_URL}/documents/{doc1_id}")
    print(f"Document: {response.json()}\n")
    
    # Update a document
    print("8. Updating a document")
    response = httpx.put(
        f"{BASE_URL}/documents/{doc1_id}",
        json={
            "metadata": {
                "category": "preferences",
                "type": "programming",
                "verified": True,
                "last_updated": "2026-02-14"
            }
        }
    )
    print(f"Update result: {response.json()}\n")
    
    # Get all documents
    print("9. Getting all documents (limited to 3)")
    response = httpx.get(f"{BASE_URL}/documents?limit=3")
    docs = response.json()
    print(f"Retrieved {len(docs)} documents:")
    for doc in docs:
        print(f"  - {doc['document'][:60]}...")
    print()
    
    # Query with metadata filter
    print("10. Querying with metadata filter (category='personal')")
    response = httpx.post(
        f"{BASE_URL}/query",
        json={
            "query_text": "tell me about myself",
            "n_results": 5,
            "where": {"category": "personal"}
        }
    )
    results = response.json()
    print(f"Found {len(results['documents'])} results with 'personal' category:")
    for i, doc in enumerate(results['documents']):
        print(f"  {i+1}. {doc}")
    print()
    
    print_section("Example Complete!")
    print("You can now explore the API at http://localhost:8000/docs")


def example_direct_storage_usage():
    """Demonstrate direct storage layer usage."""
    from storage import get_storage
    
    print_section("Direct Storage Layer Usage")
    
    storage = get_storage()
    
    # Add a document
    print("1. Adding a document directly")
    doc_id = storage.add_document(
        document="I prefer working in the morning hours.",
        metadata={"category": "work", "type": "schedule"}
    )
    print(f"Added document with ID: {doc_id}\n")
    
    # Query
    print("2. Querying documents")
    results = storage.query_documents(
        query_text="When do I work best?",
        n_results=3
    )
    print(f"Query results:")
    for i, doc in enumerate(results['documents']):
        print(f"  {i+1}. {doc}")
    print()
    
    # Count
    print("3. Counting documents")
    count = storage.count_documents()
    print(f"Total documents in collection: {count}\n")


if __name__ == "__main__":
    import sys
    
    print("ChromaDB Storage Layer - Example Script")
    print("========================================\n")
    print("Make sure the API server is running:")
    print("  python api.py\n")
    
    choice = input("Choose example:\n1. API Usage (recommended)\n2. Direct Storage Usage\n\nEnter choice (1 or 2): ")
    
    if choice == "1":
        try:
            example_api_usage()
        except httpx.ConnectError:
            print("\nError: Could not connect to API server.")
            print("Please start the server first with: python api.py")
            sys.exit(1)
    elif choice == "2":
        example_direct_storage_usage()
    else:
        print("Invalid choice. Please run again and select 1 or 2.")
