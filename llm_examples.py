"""
Examples using the LLM-Enhanced Agent for intelligent responses.
"""
from llm_agent import LLMAgent
import os


def example_smart_questions():
    """Example: Ask smart questions with natural responses."""
    print("=" * 60)
    print("EXAMPLE 1: Smart Question Answering")
    print("=" * 60)
    
    with LLMAgent() as agent:
        questions = [
            "What is my name?",
            "What is my name and what do I do?",
            "Tell me my personal identification numbers",
            "Where am I located and what are my interests?",
            "Give me a summary of all my information"
        ]
        
        for question in questions:
            print(f"\nQ: {question}")
            answer = agent.smart_ask(question, n_results=3)
            print(f"A: {answer}")
            print("-" * 60)


def example_with_sources():
    """Example: Get answers with source citations."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Answers with Sources")
    print("=" * 60)
    
    with LLMAgent() as agent:
        question = "What are my official identification numbers?"
        print(f"\nQuestion: {question}\n")
        
        answer = agent.smart_ask(
            question,
            n_results=5,
            include_sources=True
        )
        print(answer)


def example_complex_analysis():
    """Example: Complex query with multi-step search."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Complex Query Analysis")
    print("=" * 60)
    
    with LLMAgent() as agent:
        complex_queries = [
            "Tell me everything about my personal details and location",
            "What professional and personal information do you have about me?",
            "Give me a complete profile based on all stored information"
        ]
        
        for query in complex_queries:
            print(f"\nQuery: {query}")
            print("\nAnalyzing and searching...")
            
            result = agent.analyze_and_search(query, max_iterations=3)
            
            print(f"\nAnswer:\n{result['answer']}")
            print(f"\nSearch Strategy: {result['search_plan'].get('reasoning', 'N/A')}")
            print(f"\nSearches Performed:")
            for search in result['searches_performed']:
                print(f"  - '{search['query']}' -> {search['results_found']} results")
            print("\n" + "=" * 60)


def example_filtered_search():
    """Example: Search with metadata filtering."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Filtered Smart Search")
    print("=" * 60)
    
    with LLMAgent() as agent:
        # Only search in personal-info category
        print("\nSearching only in 'personal-info' category:")
        answer = agent.smart_ask(
            "What information do you have?",
            n_results=5,
            metadata_filter={"category": "personal-info"}
        )
        print(f"Answer: {answer}")
        
        print("\n" + "-" * 60)
        
        # Only search in location category
        print("\nSearching only in 'location' category:")
        answer = agent.smart_ask(
            "Tell me about the location",
            n_results=5,
            metadata_filter={"category": "location"}
        )
        print(f"Answer: {answer}")


def example_conversation():
    """Example: Have a conversation with context."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Conversational Agent")
    print("=" * 60)
    
    with LLMAgent() as agent:
        conversation_history = []
        
        messages = [
            "Hi! What's my name?",
            "Where do I live?",
            "What are my interests based on my introduction?",
            "Can you summarize everything you know about me?"
        ]
        
        for user_message in messages:
            print(f"\nYou: {user_message}")
            response, conversation_history = agent.chat(
                user_message,
                conversation_history=conversation_history
            )
            print(f"Agent: {response}")


def interactive_llm_mode():
    """Interactive mode with LLM-powered responses."""
    print("\n" + "=" * 60)
    print("INTERACTIVE LLM MODE")
    print("=" * 60)
    print("\nChat with your intelligent agent!")
    print("Type your questions (or 'quit' to exit)\n")
    
    with LLMAgent() as agent:
        conversation_history = []
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Use chat mode for conversation
                response, conversation_history = agent.chat(
                    user_input,
                    conversation_history=conversation_history
                )
                
                print(f"Agent: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}\n")


def example_comparison():
    """Compare regular search vs LLM-enhanced responses."""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Regular vs LLM-Enhanced Comparison")
    print("=" * 60)
    
    from agent import VectorDBAgent
    
    question = "What is my name and profession?"
    
    # Regular agent
    print("\nUsing Regular Agent (simple retrieval):")
    with VectorDBAgent() as regular_agent:
        answer = regular_agent.ask(question)
        print(f"Answer: {answer}")
    
    print("\n" + "-" * 60)
    
    # LLM agent
    print("\nUsing LLM Agent (intelligent response):")
    with LLMAgent() as llm_agent:
        answer = llm_agent.smart_ask(question)
        print(f"Answer: {answer}")


# ===== Main =====

if __name__ == "__main__":
    import sys
    
    print("\nLLM-Enhanced Agent Examples")
    print("=" * 60)
    
    # Check LLM provider is configured
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    print(f"\nUsing LLM Provider: {provider}")
    
    # Check API key
    if provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            print("\nError: OPENAI_API_KEY environment variable not set")
            print("\nSet it with:")
            print('  $env:OPENAI_API_KEY="your-key-here"  # PowerShell')
            print('  export OPENAI_API_KEY="your-key-here"  # Linux/Mac')
            sys.exit(1)
    elif provider == "anthropic":
        if not os.getenv("ANTHROPIC_API_KEY"):
            print("\nError: ANTHROPIC_API_KEY environment variable not set")
            sys.exit(1)
    # Ollama doesn't need API key
    
    # Check if API server is running
    try:
        from agent import VectorDBAgent
        agent = VectorDBAgent()
        agent.health_check()
        agent.close()
    except Exception as e:
        print("\nError: Could not connect to API server")
        print("Make sure the server is running: python api.py")
        print(f"Error details: {e}")
        sys.exit(1)
    
    # Run examples
    examples = {
        "1": ("Smart Question Answering", example_smart_questions),
        "2": ("Answers with Sources", example_with_sources),
        "3": ("Complex Query Analysis", example_complex_analysis),
        "4": ("Filtered Smart Search", example_filtered_search),
        "5": ("Conversational Agent", example_conversation),
        "6": ("Regular vs LLM Comparison", example_comparison),
        "7": ("Interactive LLM Mode", interactive_llm_mode),
    }
    
    if len(sys.argv) > 1:
        # Run specific example
        example_num = sys.argv[1]
        if example_num in examples:
            try:
                examples[example_num][1]()
            except ImportError as e:
                print(f"\nError: {e}")
                print(f"\nInstall required package for {provider}:")
                if provider in ["openai", "azure"]:
                    print("  pip install openai")
                elif provider == "anthropic":
                    print("  pip install anthropic")
                elif provider == "ollama":
                    print("  pip install ollama")
        else:
            print(f"Unknown example: {example_num}")
    else:
        # Show menu
        print("\nAvailable examples:")
        for num, (name, _) in examples.items():
            print(f"  {num}. {name}")
        print(f"\nRun: python llm_examples.py <number>")
        print("\nRunning quick demo...")
        
        try:
            example_smart_questions()
        except ImportError as e:
            print(f"\nError: {e}")
            print(f"\nInstall required package for {provider}:")
            if provider in ["openai", "azure"]:
                print("  pip install openai")
            elif provider == "anthropic":
                print("  pip install anthropic")
            elif provider == "ollama":
                print("  pip install ollama")
