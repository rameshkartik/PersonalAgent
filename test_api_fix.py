"""Test script to verify storage.py query fix"""
import requests

# Test 1: Health check
print("Test 1: Health check...")
response = requests.get("http://localhost:8000/")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")

# Test 2: Add a test document
print("Test 2: Adding test document...")
doc_data = {
    "document": "My name is John Doe and I live in New York City.",
    "metadata": {"category": "personal-info"}
}
response = requests.post("http://localhost:8000/documents", json=doc_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")

# Test 3: Query documents (this uses the fixed query method)
print("Test 3: Querying documents...")
query_data = {
    "query_text": "What is my name?",
    "n_results": 5
}
response = requests.post("http://localhost:8000/query", json=query_data)
print(f"Status: {response.status_code}")
response_json = response.json()
print(f"Found {len(response_json['documents'])} documents")
if response_json['documents']:
    print(f"Top result: {response_json['documents'][0][:50]}...\n")

# Test 4: LLM chat (if configured)
print("Test 4: Testing LLM chat...")
llm_data = {
    "message": "What is my name?",
    "n_results": 3
}
response = requests.post("http://localhost:8000/llm/chat", json=llm_data)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print(f"LLM Response: {response.json()['response'][:100]}...")
else:
    print(f"Error: {response.json()}")

print("\n✅ All tests completed!")
