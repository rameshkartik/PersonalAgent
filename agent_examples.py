"""
Examples of using the VectorDBAgent to interact with the API.
"""
from agent import VectorDBAgent
import json


def example_basic_operations():
    """Example: Basic CRUD operations."""
    print("=" * 60)
    print("EXAMPLE 1: Basic CRUD Operations")
    print("=" * 60)
    
    with VectorDBAgent() as agent:
        # Add a single document
        print("\n1. Adding a document...")
        doc_id = agent.add_document(
            document="I enjoy reading science fiction novels",
            metadata={"category": "hobbies", "type": "reading"}
        )
        print(f"   Created document with ID: {doc_id}")
        
        # Get the document
        print("\n2. Retrieving the document...")
        doc = agent.get_document(doc_id)
        print(f"   Document: {doc['document']}")
        print(f"   Metadata: {doc['metadata']}")
        
        # Update the document
        print("\n3. Updating the document...")
        agent.update_document(
            doc_id,
            metadata={"category": "hobbies", "type": "reading", "verified": True}
        )
        print("   ✓ Document updated")
        
        # Verify update
        updated_doc = agent.get_document(doc_id)
        print(f"   New metadata: {updated_doc['metadata']}")
        
        # Delete the document
        print("\n4. Deleting the document...")
        agent.delete_document(doc_id)
        print("   ✓ Document deleted")


def example_bulk_operations():
    """Example: Bulk document operations."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Bulk Operations")
    print("=" * 60)
    
    with VectorDBAgent() as agent:
        # Add multiple documents
        print("\n1. Adding multiple documents...")
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
        print(f"   Created {len(doc_ids)} documents")
        
        # Get statistics
        stats = agent.get_stats()
        print(f"\n2. Collection Stats:")
        print(f"   Total documents: {stats['total_documents']}")


def example_search_operations():
    """Example: Semantic search operations."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Semantic Search")
    print("=" * 60)
    
    with VectorDBAgent() as agent:
        # Basic search
        print("\n1. Basic search query:")
        results = agent.search("what is my name?", n_results=3)
        agent.print_search_results(results)
        
        # Search with metadata filter
        print("\n2. Search with metadata filter (category='personal-info'):")
        results = agent.search(
            "tell me about myself",
            n_results=5,
            where={"category": "personal-info"}
        )
        agent.print_search_results(results)
        
        # Ask a question
        print("\n3. Ask a natural language question:")
        questions = [
            "where do I live?",
            "what is my PAN number?",
            "what do I do for work?"
        ]
        
        for question in questions:
            answer = agent.ask(question)
            print(f"   Q: {question}")
            print(f"   A: {answer}\n")


def example_file_operations():
    """Example: Working with files."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: File Operations")
    print("=" * 60)
    
    with VectorDBAgent() as agent:
        # Add from file
        print("\n1. Adding documents from BulkInsert.json...")
        try:
            doc_ids = agent.add_from_file("BulkInsert.json")
            print(f"   ✓ Added {len(doc_ids)} documents from file")
        except FileNotFoundError:
            print("   ⚠ BulkInsert.json not found - skipping")
        except Exception as e:
            print(f"   ⚠ Error: {e}")


def example_metadata_filtering():
    """Example: Finding documents by metadata."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Metadata Filtering")
    print("=" * 60)
    
    with VectorDBAgent() as agent:
        # Find by category
        print("\n1. Finding documents by category='personal-info':")
        docs = agent.find_by_metadata(category="personal-info")
        for doc in docs:
            print(f"   - {doc['document']}")
        
        print(f"\n   Found {len(docs)} documents")


def example_question_answering():
    """Example: Question answering interface."""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Question Answering")
    print("=" * 60)
    
    with VectorDBAgent() as agent:
        questions = [
            "What is my name?",
            "Where do I live?",
            "What is my Aadhar number?",
            "What technologies am I interested in?",
            "Tell me about my work",
        ]
        
        print("\nAsking questions about your personal information:\n")
        for question in questions:
            answer = agent.ask(question, n_results=1)
            print(f"Q: {question}")
            print(f"A: {answer}")
            print()


def interactive_mode():
    """Example: Interactive query mode."""
    print("\n" + "=" * 60)
    print("INTERACTIVE MODE")
    print("=" * 60)
    print("\nType your questions (or 'quit' to exit):\n")
    
    with VectorDBAgent() as agent:
        while True:
            try:
                question = input("You: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if not question:
                    continue
                
                answer = agent.ask(question, n_results=2)
                print(f"Answer: {answer}\n")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}\n")


# ===== Main =====

if __name__ == "__main__":
    import sys
    
    print("\nVectorDB Agent Examples\n")
    
    # Check if API is running
    try:
        agent = VectorDBAgent()
        agent.health_check()
        agent.close()
    except Exception as e:
        print("Error: Could not connect to API server")
        print("   Make sure the server is running: python api.py")
        print(f"   Error details: {e}")
        sys.exit(1)
    
    # Run examples
    examples = {
        "1": ("Basic CRUD Operations", example_basic_operations),
        "2": ("Bulk Operations", example_bulk_operations),
        "3": ("Semantic Search", example_search_operations),
        "4": ("File Operations", example_file_operations),
        "5": ("Metadata Filtering", example_metadata_filtering),
        "6": ("Question Answering", example_question_answering),
        "7": ("Interactive Mode", interactive_mode),
    }
    
    if len(sys.argv) > 1:
        # Run specific example
        example_num = sys.argv[1]
        if example_num in examples:
            examples[example_num][1]()
        else:
            print(f"Unknown example: {example_num}")
    else:
        # Show menu
        print("Available examples:")
        for num, (name, _) in examples.items():
            print(f"  {num}. {name}")
        print("\nRun: python agent_examples.py <number>")
        print("Or run all examples:")
        
        # Run first few examples
        example_basic_operations()
        example_search_operations()
        example_question_answering()
