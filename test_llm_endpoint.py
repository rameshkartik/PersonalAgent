"""
Simple test to see the exact error from LLM endpoint.
"""
import httpx

def test_llm():
    """Test LLM endpoint and print full error."""
    try:
        client = httpx.Client(timeout=60.0)
        
        print("Testing LLM endpoint...")
        response = client.post(
            "http://localhost:8000/llm/chat",
            json={"message": "what is my name?", "n_results": 3}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Success!")
            print(f"Response: {data['response']}")
            print(f"Sources: {len(data.get('sources', []))} documents")
        else:
            print(f"\n❌ Error {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Exception: {e}")

if __name__ == "__main__":
    test_llm()
