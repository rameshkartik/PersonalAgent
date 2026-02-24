"""
Test OpenAI API key directly.
"""
from dotenv import load_dotenv
import os

load_dotenv()

def test_openai_key():
    """Test if OpenAI API key works."""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ No OPENAI_API_KEY found in .env")
        return False
        
    print(f"Testing API key: ...{api_key[-8:]}")
    
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        
        print("Sending test request to OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Say 'test successful' if you can read this"}
            ],
            max_tokens=20,
            timeout=30
        )
        
        msg = response.choices[0].message.content
        print(f"\n✅ OpenAI API key is valid!")
        print(f"Response: {msg}")
        return True
        
    except openai.AuthenticationError:
        print("\n❌ Invalid API key - authentication failed")
        return False
    except openai.RateLimitError:
        print("\n⚠️  Rate limit exceeded - but key is valid")
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_openai_key()
