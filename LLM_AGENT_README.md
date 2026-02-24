# LLM-Enhanced Agent

**Intelligent agent that combines vector search with LLM reasoning** to provide smart, natural responses.

## What's Different?

### Regular Agent (agent.py)
- ❌ Returns stored text as-is
- ❌ No reasoning or synthesis
- ❌ Can't combine multiple pieces of information
- ✅ Fast and simple

**Example:**
```python
agent.ask("what is my name?")
# Returns: "my PAN number is AIXPR3319N"  (most similar document)
```

### LLM Agent (llm_agent.py)
- ✅ **Understands context and meaning**
- ✅ **Generates natural responses**
- ✅ **Combines multiple sources**
- ✅ **Reasons about what to search**
- ✅ **Conversational memory**

**Example:**
```python
llm_agent.smart_ask("what is my name?")
# Returns: "Your name is Rameshkartik. You are a software engineer 
# with a passion for machine learning and natural language processing."
```

## Installation

### 1. Choose Your LLM Provider

**Option A: OpenAI (GPT-4, GPT-3.5)**
```bash
pip install openai
```

**Option B: Anthropic (Claude)**
```bash
pip install anthropic
```

**Option C: Ollama (Free, Local)**
```bash
pip install ollama
# Install Ollama app from https://ollama.ai
# Pull a model: ollama pull llama3.2
```

**Option D: Azure OpenAI**
```bash
pip install openai
```

### 2. Set API Key

**OpenAI:**
```powershell
# PowerShell
$env:OPENAI_API_KEY="sk-your-key-here"
$env:LLM_PROVIDER="openai"
```

**Anthropic:**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
$env:LLM_PROVIDER="anthropic"
```

**Ollama (no API key needed):**
```powershell
$env:LLM_PROVIDER="ollama"
```

## Quick Start

### Basic Usage

```python
from llm_agent import LLMAgent

with LLMAgent() as agent:
    # Ask intelligent questions
    answer = agent.smart_ask("What is my name and what do I do?")
    print(answer)
    # "Your name is Rameshkartik, and you are a software engineer..."
```

### Run Examples

```bash
# Make sure server is running
python api.py

# Run LLM examples
python llm_examples.py 1    # Smart Q&A
python llm_examples.py 5    # Conversation
python llm_examples.py 7    # Interactive mode
```

## Features

### 1. Smart Ask

Intelligent question answering with natural responses:

```python
with LLMAgent() as agent:
    # Simple question
    answer = agent.smart_ask("What is my name?")
    
    # Complex question (combines multiple sources)
    answer = agent.smart_ask(
        "Tell me my name, location, and professional interests"
    )
    
    # With sources
    answer = agent.smart_ask(
        "What are my ID numbers?",
        include_sources=True
    )
```

### 2. Analyze and Search

LLM decides what to search and how:

```python
with LLMAgent() as agent:
    result = agent.analyze_and_search(
        "Give me a complete summary of my information"
    )
    
    print(result["answer"])
    print(f"Performed {len(result['searches_performed'])} searches")
    print(f"Sources: {result['sources']}")
```

**What it does:**
1. Analyzes your question
2. Plans multiple searches if needed
3. Combines results intelligently
4. Generates comprehensive answer

### 3. Conversation Mode

Chat with memory:

```python
with LLMAgent() as agent:
    history = []
    
    # First question
    response, history = agent.chat("What's my name?", history)
    print(response)  # "Your name is Rameshkartik"
    
    # Follow-up (remembers context)
    response, history = agent.chat("And where do I live?", history)
    print(response)  # "You live in Coimbatore"
    
    # Another follow-up
    response, history = agent.chat("What else do you know?", history)
```

### 4. Filtered Search

Search specific categories:

```python
with LLMAgent() as agent:
    # Only search personal-info
    answer = agent.smart_ask(
        "What ID numbers do I have?",
        metadata_filter={"category": "personal-info"}
    )
```

## Interactive Mode

Chat interface with LLM brain:

```bash
python llm_examples.py 7
```

```
You: What is my name?
Agent: Your name is Rameshkartik. You are a software engineer with a 
       passion for machine learning and natural language processing.

You: Where do I live?
Agent: You live in Coimbatore.

You: Tell me everything about my IDs
Agent: You have two identification numbers on record:
       1. PAN Number: AIXPR3319N
       2. Aadhar Number: 3396-4206-9201
```

## Configuration

### Choose LLM Provider

```python
# OpenAI
agent = LLMAgent(llm_provider="openai", model="gpt-4o-mini")

# Anthropic Claude
agent = LLMAgent(llm_provider="anthropic", model="claude-3-5-sonnet-20241022")

# Ollama (local)
agent = LLMAgent(llm_provider="ollama", model="llama3.2")

# Azure OpenAI
agent = LLMAgent(llm_provider="azure", model="gpt-4")
```

### API Keys

**Via Environment Variables (Recommended):**
```powershell
$env:OPENAI_API_KEY="your-key"
$env:ANTHROPIC_API_KEY="your-key"
$env:AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
$env:AZURE_OPENAI_API_KEY="your-key"
```

**Via Code:**
```python
agent = LLMAgent(
    llm_provider="openai",
    api_key="sk-your-key-here"
)
```

## Comparison: Regular vs LLM Agent

| Feature | Regular Agent | LLM Agent |
|---------|--------------|-----------|
| Search | ✅ Semantic | ✅ Semantic |
| Response | Returns stored text | **Generates natural answer** |
| Multi-source | ❌ Single doc | **✅ Combines multiple docs** |
| Reasoning | ❌ No | **✅ Yes** |
| Context | ❌ No memory | **✅ Conversation memory** |
| Planning | ❌ Direct search | **✅ Analyzes & plans searches** |
| Cost | Free | Requires LLM API |
| Speed | Fast (~100ms) | Slower (~1-3s) |

## Examples

### Example 1: Simple Question

```python
from llm_agent import LLMAgent

with LLMAgent() as agent:
    answer = agent.smart_ask("What is my name?")
    print(answer)
```

**Output:**
```
Your name is Rameshkartik.
```

### Example 2: Complex Question

```python
with LLMAgent() as agent:
    answer = agent.smart_ask(
        "Tell me my name, profession, and where I live"
    )
    print(answer)
```

**Output:**
```
Your name is Rameshkartik, and you are a software engineer with a 
passion for machine learning and natural language processing. You 
live in Coimbatore.
```

### Example 3: Multi-Step Analysis

```python
with LLMAgent() as agent:
    result = agent.analyze_and_search(
        "Give me all my personal identification information"
    )
    
    print(result["answer"])
```

**Output:**
```
Here is your personal identification information:

1. PAN Number: AIXPR3319N
2. Aadhar Number: 3396-4206-9201

Both of these are official identification numbers registered in your name.
```

### Example 4: Conversation

```python
with LLMAgent() as agent:
    history = []
    
    msg1 = "Hi! What's my name?"
    resp1, history = agent.chat(msg1, history)
    print(f"You: {msg1}")
    print(f"Agent: {resp1}\n")
    
    msg2 = "What do I do?"
    resp2, history = agent.chat(msg2, history)
    print(f"You: {msg2}")
    print(f"Agent: {resp2}")
```

**Output:**
```
You: Hi! What's my name?
Agent: Hello! Your name is Rameshkartik.

You: What do I do?
Agent: You are a software engineer with a passion for machine learning 
       and natural language processing.
```

## Cost Considerations

| Provider | Cost | Speed | Quality |
|----------|------|-------|---------|
| OpenAI GPT-4o-mini | $0.15/1M tokens | Fast | Excellent |
| OpenAI GPT-4 | $10/1M tokens | Medium | Best |
| Anthropic Claude Sonnet | $3/1M tokens | Fast | Excellent |
| Ollama (Local) | **FREE** | Medium | Good |

**Typical costs for personal use:**
- 100 questions/day ≈ $0.01-0.10/day
- Using Ollama = FREE (runs locally)

## Troubleshooting

**Error: "OpenAI API key required"**
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

**Error: "Could not connect to API server"**
```bash
# Start the vector DB server first
python api.py
```

**Error: "openai not installed"**
```bash
pip install openai
```

**Using Ollama (Free Alternative):**
```bash
# Install Ollama from https://ollama.ai
# Pull a model
ollama pull llama3.2

# Set provider
$env:LLM_PROVIDER="ollama"

# Run examples
python llm_examples.py 1
```

## Files

- `llm_agent.py` - LLM-enhanced agent class
- `llm_examples.py` - Usage examples
- `LLM_AGENT_README.md` - This file

## Next Steps

1. **Set your API key** (see Installation above)
2. **Start the server**: `python api.py`
3. **Try examples**: `python llm_examples.py 1`
4. **Interactive mode**: `python llm_examples.py 7`

Now you have an **intelligent agent with LLM brain** that can understand questions, decide what to search, and generate natural responses! 🧠✨
