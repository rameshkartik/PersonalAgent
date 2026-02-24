"""
Test adding a document via POST to verify web app functionality.
"""
import httpx

def test_add_document():
    """Test adding a document to the knowledge base."""
    print("Testing POST /documents endpoint...")
    
    try:
        client = httpx.Client(timeout=10.0)
        
        # Test data
        test_doc = {
            "document": "This is a test document added from web app test",
            "metadata": {
                "category": "test",
                "type": "verification"
            }
        }
        
        response = client.post(
            "http://localhost:8000/documents",
            json=test_doc
        )
        
        if response.status_code in [200, 201]:  # Accept both 200 OK and 201 Created
            data = response.json()
            print(f"✅ Success! Document added with ID: {data['id']}")
            print(f"   Message: {data.get('message', 'N/A')}")
            
            # Verify it was added by searching
            search_response = client.post(
                "http://localhost:8000/query",
                json={"query_text": "test document", "n_results": 3}
            )
            
            if search_response.status_code == 200:
                results = search_response.json()
                if any("test document" in doc.lower() for doc in results.get("documents", [])):
                    print("✅ Document verified in search results!")
                else:
                    print("⚠️  Document added but not found in search")
            
            return True
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_add_document()
    exit(0 if success else 1)
