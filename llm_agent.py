"""
LLM-Enhanced Agent for intelligent information retrieval and response generation.
Combines vector search with LLM reasoning to provide smart answers.
"""
from agent import VectorDBAgent
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class LLMAgent(VectorDBAgent):
    """
    Enhanced agent with LLM capabilities for intelligent responses.
    
    Uses vector search to find relevant information, then LLM to generate
    natural, contextual responses.
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        timeout: float = 30.0,
        llm_provider: str = "openai",
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize LLM-enhanced agent.
        
        Args:
            base_url: Vector DB API URL
            timeout: Request timeout
            llm_provider: "openai", "anthropic", "ollama", or "azure"
            api_key: LLM API key (or set via environment variable)
            model: Model name (default depends on provider)
        """
        super().__init__(base_url, timeout)
        
        self.llm_provider = llm_provider.lower()
        self.api_key = api_key
        self.model = model
        
        # Initialize LLM client
        self._init_llm_client()
    
    def _init_llm_client(self):
        """Initialize the appropriate LLM client."""
        if self.llm_provider == "openai":
            self._init_openai()
        elif self.llm_provider == "anthropic":
            self._init_anthropic()
        elif self.llm_provider == "ollama":
            self._init_ollama()
        elif self.llm_provider == "azure":
            self._init_azure()
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")
    
    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            import openai
        except ImportError:
            raise ImportError(
                "OpenAI not installed. Run: pip install openai"
            )
        
        self.api_key = self.api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.llm_client = openai.OpenAI(api_key=self.api_key)
        self.model = self.model or "gpt-4o-mini"
    
    def _init_anthropic(self):
        """Initialize Anthropic Claude client."""
        try:
            import anthropic
        except ImportError:
            raise ImportError(
                "Anthropic not installed. Run: pip install anthropic"
            )
        
        self.api_key = self.api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.llm_client = anthropic.Anthropic(api_key=self.api_key)
        self.model = self.model or "claude-3-5-sonnet-20241022"
    
    def _init_ollama(self):
        """Initialize Ollama (local LLM) client."""
        try:
            import ollama
        except ImportError:
            raise ImportError(
                "Ollama not installed. Run: pip install ollama"
            )
        
        self.llm_client = ollama
        self.model = self.model or "llama3.2"
    
    def _init_azure(self):
        """Initialize Azure OpenAI client."""
        try:
            import openai
        except ImportError:
            raise ImportError(
                "OpenAI not installed. Run: pip install openai"
            )
        
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = self.api_key or os.getenv("AZURE_OPENAI_API_KEY")
        
        if not endpoint or not self.api_key:
            raise ValueError(
                "Azure OpenAI requires AZURE_OPENAI_ENDPOINT and "
                "AZURE_OPENAI_API_KEY environment variables."
            )
        
        self.llm_client = openai.AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=self.api_key,
            api_version="2024-02-15-preview"
        )
        self.model = self.model or "gpt-4"
    
    def _call_llm(self, messages: List[Dict[str, str]]) -> str:
        """Call the LLM with messages and return response."""
        if self.llm_provider == "openai" or self.llm_provider == "azure":
            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                timeout=30.0  # 30 second timeout
            )
            return response.choices[0].message.content
        
        elif self.llm_provider == "anthropic":
            # Anthropic uses different format
            system_msg = next((m["content"] for m in messages if m["role"] == "system"), None)
            user_messages = [m for m in messages if m["role"] != "system"]
            
            response = self.llm_client.messages.create(
                model=self.model,
                max_tokens=500,
                system=system_msg,
                messages=user_messages,
                timeout=30.0  # 30 second timeout
            )
            return response.content[0].text
        
        elif self.llm_provider == "ollama":
            response = self.llm_client.chat(
                model=self.model,
                messages=messages
            )
            return response['message']['content']
        
        else:
            raise ValueError(f"Unsupported provider: {self.llm_provider}")
    
    def smart_ask(
        self,
        question: str,
        n_results: int = 3,
        include_sources: bool = False,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Ask a question and get an LLM-generated intelligent response.
        
        The agent will:
        1. Search the vector DB for relevant information
        2. Use LLM to generate a natural, contextual answer
        
        Args:
            question: The question to ask
            n_results: Number of documents to retrieve for context
            include_sources: Include source documents in response
            metadata_filter: Optional metadata filter for search
            
        Returns:
            LLM-generated answer based on your stored information
        """
        # Search for relevant context
        search_results = self.search(
            query=question,
            n_results=n_results,
            where=metadata_filter
        )
        
        # Build context from search results
        if not search_results["documents"]:
            return self._call_llm([
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"I don't have any information to answer: {question}"}
            ])
        
        context_parts = []
        for i, doc in enumerate(search_results["documents"], 1):
            context_parts.append(f"[{i}] {doc}")
        
        context = "\n".join(context_parts)
        
        # Create LLM prompt
        system_prompt = """You are a helpful personal assistant with access to the user's stored information.
Answer questions based ONLY on the provided context. Be natural and conversational.
If the context doesn't contain the answer, say so clearly."""
        
        user_prompt = f"""Context from user's personal knowledge base:
{context}

Question: {question}

Please provide a clear, natural answer based on the context above."""
        
        # Get LLM response
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        answer = self._call_llm(messages)
        
        # Add sources if requested
        if include_sources:
            sources = "\n\nSources:\n" + "\n".join(
                f"- {doc}" for doc in search_results["documents"]
            )
            answer += sources
        
        return answer
    
    def analyze_and_search(
        self,
        query: str,
        max_iterations: int = 3
    ) -> Dict[str, Any]:
        """
        Use LLM to analyze the query and decide what to search for.
        
        The LLM will:
        1. Break down complex questions
        2. Decide what information to fetch
        3. Perform multiple searches if needed
        4. Synthesize a comprehensive answer
        
        Args:
            query: User's question or request
            max_iterations: Maximum search iterations
            
        Returns:
            Dictionary with answer, searches performed, and sources
        """
        # Ask LLM to plan the search strategy
        planning_prompt = f"""Analyze this question and determine what information to search for:
"{query}"

Provide a search strategy as a JSON object with this format:
{{
    "search_queries": ["query1", "query2"],
    "metadata_filters": [{{"category": "personal-info"}}, null],
    "reasoning": "Why these searches are needed"
}}

Limit to {max_iterations} searches maximum."""
        
        messages = [
            {"role": "system", "content": "You are a search planning assistant. Output valid JSON only."},
            {"role": "user", "content": planning_prompt}
        ]
        
        # Get search plan
        try:
            import json
            plan_text = self._call_llm(messages)
            # Extract JSON from response
            if "```json" in plan_text:
                plan_text = plan_text.split("```json")[1].split("```")[0]
            elif "```" in plan_text:
                plan_text = plan_text.split("```")[1].split("```")[0]
            
            plan = json.loads(plan_text.strip())
        except Exception as e:
            # Fallback to simple search
            plan = {
                "search_queries": [query],
                "metadata_filters": [None],
                "reasoning": f"Using direct search due to planning error: {e}"
            }
        
        # Perform searches
        all_results = []
        searches_performed = []
        
        for i, search_query in enumerate(plan.get("search_queries", [query])):
            metadata_filter = None
            if i < len(plan.get("metadata_filters", [])):
                metadata_filter = plan["metadata_filters"][i]
            
            results = self.search(
                query=search_query,
                n_results=3,
                where=metadata_filter
            )
            
            if results["documents"]:
                all_results.extend(results["documents"])
                searches_performed.append({
                    "query": search_query,
                    "filter": metadata_filter,
                    "results_found": len(results["documents"])
                })
        
        # Remove duplicates
        unique_results = list(dict.fromkeys(all_results))
        
        # Generate comprehensive answer
        context = "\n".join(f"[{i+1}] {doc}" for i, doc in enumerate(unique_results))
        
        final_prompt = f"""Based on the following information from the user's knowledge base, answer this question:

Question: {query}

Information available:
{context}

Provide a comprehensive, natural answer."""
        
        messages = [
            {"role": "system", "content": "You are a helpful personal assistant."},
            {"role": "user", "content": final_prompt}
        ]
        
        answer = self._call_llm(messages)
        
        return {
            "answer": answer,
            "searches_performed": searches_performed,
            "sources": unique_results,
            "search_plan": plan
        }
    
    def chat(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        n_results: int = 3
    ) -> tuple[str, List[Dict[str, str]]]:
        """
        Have a conversation with context from your knowledge base.
        
        Args:
            message: User's message
            conversation_history: Previous conversation messages
            n_results: Number of documents to retrieve
            
        Returns:
            Tuple of (response, updated_conversation_history)
        """
        if conversation_history is None:
            conversation_history = []
        
        # Search for relevant context
        search_results = self.search(query=message, n_results=n_results)
        
        # Build context
        if search_results["documents"]:
            context = "\n".join(f"- {doc}" for doc in search_results["documents"])
            context_message = f"\nRelevant information from knowledge base:\n{context}"
        else:
            context_message = "\nNo relevant information found in knowledge base."
        
        # Add to conversation
        messages = [
            {"role": "system", "content": "You are a helpful personal assistant with access to the user's stored information. Use the provided context when relevant."}
        ]
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Add current message with context
        messages.append({
            "role": "user",
            "content": message + context_message
        })
        
        # Get response
        response = self._call_llm(messages)
        
        # Update history (without context injection)
        conversation_history.append({"role": "user", "content": message})
        conversation_history.append({"role": "assistant", "content": response})
        
        return response, conversation_history


# ===== Example Usage =====

if __name__ == "__main__":
    import sys
    
    print("\n" + "=" * 60)
    print("LLM-Enhanced Agent Demo")
    print("=" * 60)
    
    # Choose provider
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    if provider not in ["openai", "anthropic", "ollama", "azure"]:
        print(f"\nError: Invalid LLM_PROVIDER '{provider}'")
        print("Set environment variable LLM_PROVIDER to one of:")
        print("  - openai (requires OPENAI_API_KEY)")
        print("  - anthropic (requires ANTHROPIC_API_KEY)")
        print("  - ollama (local, free)")
        print("  - azure (requires AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY)")
        sys.exit(1)
    
    try:
        # Create LLM agent
        print(f"\nInitializing {provider} LLM agent...")
        agent = LLMAgent(llm_provider=provider)
        
        # Test connection
        health = agent.health_check()
        print(f"Vector DB Status: {health['status']}")
        
        print("\n" + "=" * 60)
        print("INTERACTIVE LLM AGENT")
        print("=" * 60)
        print("\nAsk me anything about your stored information!")
        print("Commands:")
        print("  - Type your question to get an intelligent answer")
        print("  - Type 'help' for usage tips")
        print("  - Type 'quit' or 'exit' to end session")
        print("\n" + "=" * 60 + "\n")
        
        conversation_history = []
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Handle commands
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                    print("\nGoodbye! Your information is safely stored.")
                    break
                
                if user_input.lower() == 'help':
                    print("\nUsage Tips:")
                    print("  - Ask natural questions: 'What is my name?'")
                    print("  - Request summaries: 'Tell me everything about my IDs'")
                    print("  - Ask about specific info: 'Where do I live?'")
                    print("  - Complex queries: 'Give me a complete profile'")
                    print()
                    continue
                
                # Process the question with LLM
                print("\nThinking...", end="", flush=True)
                
                # Use chat mode for conversational context
                response, conversation_history = agent.chat(
                    user_input,
                    conversation_history=conversation_history,
                    n_results=3
                )
                
                print("\r" + " " * 15 + "\r", end="")  # Clear "Thinking..."
                print(f"Agent: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nSession ended. Goodbye!")
                break
            except Exception as e:
                print(f"\nError processing your question: {e}")
                print("Please try again or type 'quit' to exit.\n")
        
        agent.close()
        
    except ImportError as e:
        print(f"\nError: {e}")
        print(f"\nTo use {provider}, install required package:")
        if provider == "openai" or provider == "azure":
            print("  pip install openai")
        elif provider == "anthropic":
            print("  pip install anthropic")
        elif provider == "ollama":
            print("  pip install ollama")
        sys.exit(1)
    
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
