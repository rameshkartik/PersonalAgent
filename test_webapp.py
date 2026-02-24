"""
Test script to verify web app setup and API endpoints.
"""
import sys
import time

def test_api_server():
    """Test if API server is running."""
    print("🔍 Testing API Server...")
    try:
        import httpx
        client = httpx.Client(timeout=5.0)
        
        # Test health endpoint
        response = client.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ API server is running")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Version: {data.get('version')}")
            return True
        else:
            print(f"❌ API server returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API server: {e}")
        print(f"   Start the server with: python api.py")
        return False

def test_llm_configuration():
    """Test if LLM is configured."""
    print("\n🧠 Testing LLM Configuration...")
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        
        llm_provider = os.getenv('LLM_PROVIDER', 'openai')
        print(f"   Provider: {llm_provider}")
        
        if llm_provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                print(f"✅ OpenAI API key is set (ends with: ...{api_key[-4:]})")
                return True
            else:
                print("❌ OPENAI_API_KEY not set in .env file")
                return False
        elif llm_provider == 'anthropic':
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                print(f"✅ Anthropic API key is set")
                return True
            else:
                print("❌ ANTHROPIC_API_KEY not set in .env file")
                return False
        elif llm_provider == 'ollama':
            print("✅ Ollama doesn't require API key")
            return True
        else:
            print(f"❌ Unknown LLM provider: {llm_provider}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking LLM configuration: {e}")
        return False

def test_llm_endpoint():
    """Test LLM endpoint."""
    print("\n💬 Testing LLM Endpoint...")
    try:
        import httpx
        client = httpx.Client(timeout=30.0)
        
        response = client.post(
            "http://localhost:8000/llm/chat",
            json={"message": "test", "n_results": 1}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ LLM endpoint is working")
            print(f"   Response received: {len(data.get('response', ''))} characters")
            return True
        else:
            print(f"❌ LLM endpoint returned status code: {response.status_code}")
            error = response.json()
            print(f"   Error: {error.get('detail', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing LLM endpoint: {e}")
        return False

def test_vector_db():
    """Test vector database."""
    print("\n💾 Testing Vector Database...")
    try:
        import httpx
        client = httpx.Client(timeout=5.0)
        
        response = client.get("http://localhost:8000/stats")
        if response.status_code == 200:
            data = response.json()
            print("✅ Vector database is accessible")
            print(f"   Total documents: {data.get('total_documents')}")
            print(f"   Collection: {data.get('collection_name')}")
            return True
        else:
            print(f"❌ Stats endpoint returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing vector database: {e}")
        return False

def test_simple_search():
    """Test simple search endpoint."""
    print("\n🔎 Testing Simple Search...")
    try:
        import httpx
        client = httpx.Client(timeout=10.0)
        
        response = client.post(
            "http://localhost:8000/query",
            json={"query_text": "test", "n_results": 3}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Simple search is working")
            print(f"   Results found: {len(data.get('documents', []))}")
            return True
        else:
            print(f"❌ Search endpoint returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing search: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Web App Setup Test")
    print("=" * 60)
    
    results = {
        "API Server": test_api_server(),
        "Vector Database": False,
        "Simple Search": False,
        "LLM Configuration": False,
        "LLM Endpoint": False
    }
    
    if results["API Server"]:
        results["Vector Database"] = test_vector_db()
        results["Simple Search"] = test_simple_search()
        results["LLM Configuration"] = test_llm_configuration()
        
        if results["LLM Configuration"]:
            results["LLM Endpoint"] = test_llm_endpoint()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"{status} {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Web app is ready to use.")
        print("\n📝 Next steps:")
        print("   1. Open web_app.html in your browser")
        print("   2. Try adding some information")
        print("   3. Ask questions using the LLM Agent tab")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        
        if not results["API Server"]:
            print("\n🔧 To fix:")
            print("   1. Run: python api.py")
            print("   2. Wait for server to start")
            print("   3. Run this test again")
        
        elif not results["LLM Configuration"]:
            print("\n🔧 To fix:")
            print("   1. Edit .env file")
            print("   2. Add: OPENAI_API_KEY=your-key-here")
            print("   3. Or use: LLM_PROVIDER=ollama (free)")
        
        elif not results["LLM Endpoint"]:
            print("\n🔧 To fix:")
            print("   1. Make sure LLM dependencies are installed:")
            print("      pip install openai")
            print("   2. Restart the API server")
    
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
