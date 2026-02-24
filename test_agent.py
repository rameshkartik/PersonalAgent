"""Quick test of the VectorDBAgent."""
from agent import VectorDBAgent

# Create and test the agent
with VectorDBAgent() as agent:
    print("=" * 60)
    print("VectorDB Agent Demo")
    print("=" * 60)
    
    # 1. Health check
    print("\n1. Health Check:")
    health = agent.health_check()
    print(f"   Status: {health['status']}")
    
    # 2. Get stats
    print("\n2. Collection Statistics:")
    stats = agent.get_stats()
    print(f"   Total Documents: {stats['total_documents']}")
    
    # 3. Search for information
    print("\n3. Semantic Search - 'what is my name?':")
    results = agent.search("what is my name?", n_results=2)
    for i, doc in enumerate(results["documents"][:2], 1):
        print(f"   {i}. {doc[:80]}...")
    
    # 4. Ask questions
    print("\n4. Question Answering:")
    questions = [
        "Where do I live?",
        "What is my PAN number?",
        "What is my name?"
    ]
    for q in questions:
        answer = agent.ask(q, n_results=1)
        print(f"   Q: {q}")
        print(f"   A: {answer[:100]}...")
        print()
    
    print("=" * 60)
    print("✓ Agent Demo Completed Successfully!")
    print("=" * 60)
