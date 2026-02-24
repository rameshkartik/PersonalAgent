"""Test the storage layer directly"""
from storage import VectorDBStorage
import uuid

print("Creating storage...")
storage = VectorDBStorage()

print("Adding test document...")
doc_id = storage.add_document(
    document="Test document about Rameshkartik",
    metadata={"category": "test"},
    doc_id=str(uuid.uuid4())
)
print(f"Added document with ID: {doc_id}")

print("\nQuerying...")
try:
    results = storage.query_documents("what is the name?", n_results=1)
    print(f"Query successful!")
    print(f"Results: {results}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
