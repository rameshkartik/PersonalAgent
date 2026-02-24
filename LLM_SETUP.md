# Quick Setup: LLM-Enhanced Agent

## What You Get

An intelligent agent that:
- ✅ **Understands** what you're asking
- ✅ **Decides** what information to fetch from your database
- ✅ **Generates** natural, intelligent responses
- ✅ **Remembers** conversation context

## 3-Step Setup

### Step 1: Choose LLM Provider

Pick one:

**Option A: OpenAI (Easiest, Paid)**
```powershell
pip install openai
$env:OPENAI_API_KEY="sk-your-key-here"
$env:LLM_PROVIDER="openai"
```

**Option B: Ollama (FREE, Local)**
```powershell
# Download from https://ollama.ai
# After installing Ollama app:
ollama pull llama3.2
pip install ollama
$env:LLM_PROVIDER="ollama"
```

**Option C: Anthropic Claude (Paid)**
```powershell
pip install anthropic
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
$env:LLM_PROVIDER="anthropic"
```

### Step 2: Start API Server

```bash
python api.py
```

### Step 3: Use LLM Agent

**Quick Test:**
```bash
python llm_agent.py
```

**Interactive Mode:**
```bash
python llm_examples.py 7
```

**In Your Code:**
```python
from llm_agent import LLMAgent

with LLMAgent() as agent:
    answer = agent.smart_ask("What is my name and profession?")
    print(answer)
```

## Example Usage

### Before (Regular Agent)

```python
from agent import VectorDBAgent

agent = VectorDBAgent()
answer = agent.ask("what is my name?")
print(answer)
# Output: "my PAN number is AIXPR3319N"  ❌ Wrong document!
```

### After (LLM Agent)

```python
from llm_agent import LLMAgent

agent = LLMAgent()
answer = agent.smart_ask("what is my name?")
print(answer)
# Output: "Your name is Rameshkartik. You are a software engineer 
#          with a passion for machine learning and NLP." ✅ Perfect!
```

## Key Features

### 1. Smart Question Answering

```python
agent.smart_ask("Tell me everything about my IDs")
```

**LLM will:**
1. Search for "identification" related docs
2. Find PAN and Aadhar numbers
3. Generate: "You have two IDs: PAN (AIXPR3319N) and Aadhar (3396-4206-9201)"

### 2. Complex Analysis

```python
result = agent.analyze_and_search(
    "Give me a complete profile of myself"
)
```

**LLM will:**
1. Plan multiple searches (name, location, work, IDs)
2. Fetch info from each category
3. Synthesize comprehensive response

### 3. Conversation Mode

```python
history = []
resp1, history = agent.chat("Hi! What's my name?", history)
resp2, history = agent.chat("Where do I live?", history)
resp3, history = agent.chat("Summarize what you know", history)
```

**LLM remembers** previous context!

## Cost

| Provider | Cost | Speed |
|----------|------|-------|
| **Ollama** | **FREE** | Medium |
| OpenAI GPT-4o-mini | ~$0.01/day | Fast |
| OpenAI GPT-4 | ~$0.10/day | Medium |
| Claude Sonnet | ~$0.03/day | Fast |

For personal use (100 questions/day), cost is negligible with OpenAI mini.

**Recommended: Start with Ollama (FREE)**, upgrade to OpenAI if you need better quality.

## Examples to Try

```bash
# Smart questions
python llm_examples.py 1

# Conversation
python llm_examples.py 5

# Interactive chat
python llm_examples.py 7
```

## Interactive Chat Session

```
You: What is my name?
Agent: Your name is Rameshkartik.

You: What do I do?
Agent: You are a software engineer with a passion for machine learning 
       and natural language processing.

You: Where do I live?
Agent: You live in Coimbatore.

You: Give me all my ID numbers
Agent: Your identification numbers are:
       - PAN: AIXPR3319N
       - Aadhar: 3396-4206-9201
```

## Troubleshooting

**"OpenAI API key required"**
```powershell
$env:OPENAI_API_KEY="sk-..."
```

**"Could not connect to API"**
```bash
python api.py  # Run in separate terminal
```

**Want FREE option?** Use Ollama:
```bash
# Install from https://ollama.ai
ollama pull llama3.2
pip install ollama
$env:LLM_PROVIDER="ollama"
python llm_agent.py
```

## What's Happening Under the Hood

```
Your question: "What is my name and profession?"
        ↓
LLM Brain analyzes question
        ↓
Agent searches DB for: "name", "profession", "work"
        ↓
Finds: "I am Rameshkartik, a software engineer..."
        ↓
LLM generates natural response:
"Your name is Rameshkartik, and you work as a software engineer 
 with expertise in machine learning and NLP."
```

## Ready to Go!

```bash
# 1. Install LLM package (pick one)
pip install openai      # or: pip install ollama

# 2. Set API key (if using OpenAI)
$env:OPENAI_API_KEY="sk-..."

# 3. Start server
python api.py

# 4. Try it!
python llm_agent.py
```

Now you have an **intelligent agent with LLM brain**! 🧠✨

See [LLM_AGENT_README.md](LLM_AGENT_README.md) for full documentation.
