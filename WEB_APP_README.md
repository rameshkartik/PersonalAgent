# Personal Knowledge Base - Web Application

A beautiful single-page web application for managing your personal information with AI-powered search using the LLM agent.

## 🌟 Features

### 📝 Add Information
- Store personal information, facts, and knowledge
- Organize with categories (Personal Info, Work, Education, etc.)
- Add custom tags for better organization

### 🔍 Search & Query
Two powerful search modes:

1. **LLM Agent** - Intelligent, conversational search
   - Ask natural questions: "What is my name?"
   - Get smart, synthesized answers
   - Combines multiple sources automatically

2. **Simple Search** - Direct vector search
   - Fast semantic search
   - Returns relevant documents with scores
   - No LLM processing

### 📊 Real-time Stats
- See total documents stored
- Track number of searches
- Monitor API status

## 🚀 Quick Start

### 1. Start the API Server

```bash
python api.py
```

The server must be running on `http://localhost:8000`

### 2. Open the Web App

Simply open the HTML file in your browser:

**Option A: Double-click**
```
Double-click web_app.html
```

**Option B: Using Python**
```bash
python -m http.server 8080
```
Then visit: `http://localhost:8080/web_app.html`

**Option C: Using VS Code**
- Right-click `web_app.html`
- Select "Open with Live Server" (if installed)

### 3. Start Using!

- **Add data**: Fill the form and click "Add to Knowledge Base"
- **Search**: Switch between LLM Agent and Simple Search tabs
- **Ask questions**: Type naturally like "What are my skills?"

## 💡 Usage Examples

### Adding Information

```
Information: I am a Python developer with 5 years of experience
Category: Work
Type: role
```

```
Information: I graduated from Stanford University in 2018
Category: Education  
Type: degree
```

### LLM Agent Queries

Try asking:
- "What is my name?"
- "Tell me about my education"
- "What are my professional skills?"
- "Give me a summary of my information"
- "Where do I live?"

### Simple Search

Search for:
- "work experience"
- "education" 
- "personal information"
- "skills"

## 🎨 Interface Guide

### Add Information Card (Left)
- **Information**: The actual data/fact you want to store
- **Category**: Predefined categories for organization
- **Type/Tag**: Custom tags for better filtering

### Search Card (Right)
- **LLM Agent Tab**: AI-powered intelligent responses
- **Simple Search Tab**: Direct vector search results
- **Results Area**: Shows responses and search results

### Stats Bar (Bottom)
- **Documents**: Total number of stored items
- **Searches**: Number of queries performed this session
- **API Status**: Green = Connected, Red = Disconnected

## 🔧 Configuration

### API URL
Default: `http://localhost:8000`

To change, edit in `web_app.html`:
```javascript
const API_URL = 'http://your-server:8000';
```

### LLM Provider
The web app uses the LLM configuration from your `.env` file.

Make sure you have:
```bash
OPENAI_API_KEY=your-key-here  # or other LLM provider
LLM_PROVIDER=openai
```

## 🎯 Features Breakdown

### 1. Add Documents (POST)
- Endpoint: `POST /documents`
- Stores information with metadata
- Returns document ID
- Updates stats automatically

### 2. LLM Chat (POST)
- Endpoint: `POST /llm/chat`
- Intelligent AI responses
- Combines multiple sources
- Natural language answers

### 3. Simple Search (POST)
- Endpoint: `POST /query`
- Semantic vector search
- Returns top N results
- Shows relevance scores

### 4. Statistics (GET)
- Endpoint: `GET /stats`
- Real-time document count
- Collection information

## 🛠️ Troubleshooting

### "API server is not running"
**Solution:** Start the API server
```bash
python api.py
```

### "LLM configuration error"
**Solution:** Set your API key in `.env`
```bash
OPENAI_API_KEY=sk-your-key-here
```

### No results from search
**Solution:** Add some documents first using the form

### CORS errors
**Solution:** Make sure CORS is enabled in `api.py` (already configured)

## 📱 Browser Compatibility

Works on all modern browsers:
- ✅ Chrome
- ✅ Firefox
- ✅ Safari
- ✅ Edge

## 🔒 Security Notes

**For Development Only:**
- CORS is set to allow all origins (`*`)
- No authentication required
- Data stored in local vector database

**For Production:**
- Add authentication
- Restrict CORS origins
- Use HTTPS
- Add rate limiting

## 🎨 Customization

### Change Colors
Edit the CSS variables in `web_app.html`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Add Categories
Add to the select dropdown:
```html
<option value="your-category">Your Category</option>
```

### Modify Results Display
Edit the `displayLLMResponse` or `displaySearchResults` functions.

## 📊 API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/stats` | GET | Get statistics |
| `/documents` | POST | Add document |
| `/query` | POST | Search documents |
| `/llm/chat` | POST | LLM intelligent response |

## 🚀 Next Steps

1. **Add more data** - Build your knowledge base
2. **Try different queries** - Test LLM vs simple search
3. **Organize with categories** - Use tags for better filtering
4. **Export data** - Use API endpoints to backup
5. **Integrate with apps** - Use the same API in other tools

## 💻 Files

- `web_app.html` - Single-page application (this file)
- `api.py` - FastAPI backend server
- `llm_agent.py` - LLM agent with intelligence
- `agent.py` - Basic agent for simple operations

## 📖 Related Documentation

- [README.md](README.md) - Main project documentation
- [LLM_AGENT_README.md](LLM_AGENT_README.md) - LLM agent details
- [AGENT_README.md](AGENT_README.md) - Agent documentation

---

**Built with ❤️ using FastAPI, Qdrant, and OpenAI**

Enjoy your AI-powered personal knowledge base! 🧠✨
