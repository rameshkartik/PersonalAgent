# Architecture Diagrams - Mermaid Code

## 1. System Architecture Diagram

```mermaid
graph TB
    subgraph "Frontend Layer"
        WebApp[Web Application<br/>web_app.html<br/>JavaScript + HTML/CSS]
    end
    
    subgraph "API Layer"
        API[FastAPI REST API<br/>api.py<br/>Port 8000]
        
        subgraph "API Endpoints"
            CRUD[CRUD Endpoints<br/>POST/GET/PUT/DELETE<br/>/documents]
            Search[Search Endpoints<br/>POST /query<br/>POST /search/metadata]
            LLM[LLM Endpoints<br/>POST /llm/chat<br/>POST /llm/smart-ask]
            System[System Endpoints<br/>GET /<br/>GET /stats]
        end
    end
    
    subgraph "Business Logic Layer"
        Storage[VectorDBStorage<br/>storage.py<br/>Manages embeddings & queries]
        Agent[VectorDBAgent<br/>agent.py<br/>HTTP client for API]
        LLMAgent[LLMAgent<br/>llm_agent.py<br/>LLM-enhanced queries]
    end
    
    subgraph "Data Layer"
        Qdrant[(Qdrant Vector DB<br/>Local File-based<br/>./vector_data/)]
        Embeddings[Sentence Transformers<br/>all-MiniLM-L6-v2<br/>384-dim vectors]
    end
    
    subgraph "External Services"
        OpenAI[OpenAI API<br/>GPT-4o-mini<br/>LLM Intelligence]
    end
    
    subgraph "Configuration"
        Env[.env File<br/>API Keys<br/>Settings]
        Config[config.py<br/>Configuration Manager]
    end
    
    %% Frontend connections
    WebApp -->|HTTP Requests<br/>JSON| API
    
    %% API to Endpoints
    API --> CRUD
    API --> Search
    API --> LLM
    API --> System
    
    %% API to Business Logic
    CRUD --> Storage
    Search --> Storage
    LLM --> Storage
    System --> Storage
    LLM -->|Chat Completions| OpenAI
    
    %% Agent connections
    Agent -->|HTTP Client| API
    LLMAgent -->|Extends| Agent
    LLMAgent -->|Direct Access| OpenAI
    
    %% Business Logic to Data
    Storage --> Embeddings
    Storage --> Qdrant
    Embeddings -->|Generate Vectors| Qdrant
    
    %% Configuration
    Config --> Env
    API --> Config
    Storage --> Config
    LLMAgent --> Config
    
    %% Styling
    classDef frontend fill:#9b59b6,stroke:#8e44ad,color:#fff
    classDef api fill:#3498db,stroke:#2980b9,color:#fff
    classDef logic fill:#2ecc71,stroke:#27ae60,color:#fff
    classDef data fill:#e74c3c,stroke:#c0392b,color:#fff
    classDef external fill:#f39c12,stroke:#d68910,color:#fff
    classDef config fill:#95a5a6,stroke:#7f8c8d,color:#fff
    
    class WebApp frontend
    class API,CRUD,Search,LLM,System api
    class Storage,Agent,LLMAgent logic
    class Qdrant,Embeddings data
    class OpenAI external
    class Env,Config config
```

## 2. Request Flow Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant WebApp as Web App<br/>(web_app.html)
    participant API as FastAPI Server<br/>(api.py)
    participant Storage as VectorDBStorage<br/>(storage.py)
    participant Embeddings as Sentence Transformers<br/>(all-MiniLM-L6-v2)
    participant Qdrant as Qdrant Vector DB<br/>(./vector_data)
    participant OpenAI as OpenAI API<br/>(GPT-4o-mini)
    
    rect rgb(230, 240, 255)
        Note over User,OpenAI: Scenario 1: Adding Information
        User->>WebApp: Fill form & click "Add"
        WebApp->>API: POST /documents<br/>{document, metadata}
        API->>Storage: add_document()
        Storage->>Embeddings: encode(document)
        Embeddings-->>Storage: [384-dim vector]
        Storage->>Qdrant: upsert(vector, metadata)
        Qdrant-->>Storage: Success
        Storage-->>API: document_id
        API-->>WebApp: 201 Created + ID
        WebApp-->>User: ✓ Success message
    end
    
    rect rgb(240, 255, 240)
        Note over User,OpenAI: Scenario 2: Simple Search
        User->>WebApp: Enter search query
        WebApp->>API: POST /query<br/>{query_text, n_results}
        API->>Storage: query_documents()
        Storage->>Embeddings: encode(query)
        Embeddings-->>Storage: [384-dim vector]
        Storage->>Qdrant: query_points(vector)
        Qdrant-->>Storage: Similar documents
        Storage-->>API: {documents, scores}
        API-->>WebApp: JSON results
        WebApp-->>User: Display matches
    end
    
    rect rgb(255, 240, 255)
        Note over User,OpenAI: Scenario 3: LLM-Enhanced Search
        User->>WebApp: Ask question in LLM tab
        WebApp->>API: POST /llm/chat<br/>{message}
        API->>Storage: query_documents(message)
        Storage->>Embeddings: encode(message)
        Embeddings-->>Storage: [query vector]
        Storage->>Qdrant: query_points(vector)
        Qdrant-->>Storage: Relevant docs
        Storage-->>API: {documents}
        API->>OpenAI: chat.completions.create()<br/>system + context + question
        OpenAI-->>API: Natural language answer
        API-->>WebApp: {response, sources}
        WebApp-->>User: Smart conversational answer
    end
```

## 3. Component Relationships Diagram

```mermaid
graph LR
    subgraph "User Interfaces"
        W[Web App<br/>Browser UI]
        C[CLI<br/>llm_agent.py]
        P[Python Scripts<br/>agent.py]
    end
    
    subgraph "Core Components"
        A[API Server<br/>FastAPI]
        S[Storage Layer<br/>Qdrant + Embeddings]
        L[LLM Service<br/>OpenAI]
    end
    
    W -->|HTTP| A
    C -->|HTTP| A
    P -->|HTTP| A
    
    A -->|Direct Access| S
    A -->|API Calls| L
    
    S -->|Store/Query| DB[(Vector DB)]
    
    style W fill:#9b59b6,color:#fff
    style C fill:#9b59b6,color:#fff
    style P fill:#9b59b6,color:#fff
    style A fill:#3498db,color:#fff
    style S fill:#2ecc71,color:#fff
    style L fill:#f39c12,color:#fff
    style DB fill:#e74c3c,color:#fff
```

## 4. Technology Stack Diagram

```mermaid
graph TD
    subgraph "Frontend"
        HTML[HTML5]
        CSS[CSS3<br/>Gradients]
        JS[JavaScript ES6+<br/>Fetch API]
    end
    
    subgraph "Backend"
        FastAPI[FastAPI 0.109.0<br/>Async Python]
        Uvicorn[Uvicorn 0.27.0<br/>ASGI Server]
        Pydantic[Pydantic 2.5.3<br/>Validation]
    end
    
    subgraph "ML/AI"
        ST[Sentence Transformers 2.3.1<br/>all-MiniLM-L6-v2]
        OpenAI[OpenAI SDK<br/>GPT-4o-mini]
    end
    
    subgraph "Database"
        Qdrant[Qdrant Client 1.7.3<br/>Vector Database]
        Files[Local File Storage<br/>./vector_data/]
    end
    
    subgraph "Tools"
        HTTPX[HTTPX 0.26.0<br/>HTTP Client]
        Dotenv[python-dotenv 1.0.0<br/>Config Management]
    end
    
    HTML --> JS
    CSS --> JS
    
    FastAPI --> Uvicorn
    FastAPI --> Pydantic
    
    FastAPI --> ST
    FastAPI --> OpenAI
    
    ST --> Qdrant
    Qdrant --> Files
    
    FastAPI --> HTTPX
    FastAPI --> Dotenv
    
    style HTML fill:#e74c3c,color:#fff
    style CSS fill:#e74c3c,color:#fff
    style JS fill:#e74c3c,color:#fff
    style FastAPI fill:#3498db,color:#fff
    style Uvicorn fill:#3498db,color:#fff
    style Pydantic fill:#3498db,color:#fff
    style ST fill:#9b59b6,color:#fff
    style OpenAI fill:#f39c12,color:#fff
    style Qdrant fill:#2ecc71,color:#fff
    style Files fill:#2ecc71,color:#fff
```

---

## How to Use These Diagrams

### Option 1: VS Code (Already Rendered)
The diagrams above are already rendered in VS Code's Mermaid preview.

### Option 2: Online Mermaid Editors
1. Copy any diagram code block from above
2. Visit: https://mermaid.live/
3. Paste the code
4. View/export the diagram

### Option 3: Markdown Viewers
- GitHub/GitLab - Renders automatically in README.md
- Notion - Supports Mermaid blocks
- Obsidian - With Mermaid plugin

### Option 4: Export as Image
Use mermaid-cli:
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i ARCHITECTURE.md -o architecture.png
```

---

## Diagram Descriptions

### 1. System Architecture
Shows all components, layers, and their relationships. Use this for understanding the overall system structure.

**Key Components:**
- **Purple**: Frontend (Web App)
- **Blue**: API Layer (FastAPI endpoints)
- **Green**: Business Logic (Storage, Agents)
- **Red**: Data Layer (Qdrant, Embeddings)
- **Orange**: External Services (OpenAI)
- **Gray**: Configuration

### 2. Request Flow Sequence
Shows step-by-step flow of three common operations:
1. **Adding Information** (Blue background)
2. **Simple Search** (Green background)
3. **LLM-Enhanced Search** (Purple background)

### 3. Component Relationships
Simplified view showing how users interact with the system through different interfaces.

### 4. Technology Stack
Complete technology stack with version numbers for all major dependencies.

---

## System Statistics

**Current State:**
- **Total Documents**: 8
- **Collection**: personal_info
- **Vector Dimensions**: 384
- **API Endpoints**: 12
- **LLM Provider**: OpenAI GPT-4o-mini
- **Database**: Qdrant (local file-based)

**File Breakdown:**
```
Frontend:     1 file  (web_app.html)
API:          1 file  (api.py) 
Storage:      1 file  (storage.py)
Agents:       2 files (agent.py, llm_agent.py)
Models:       1 file  (models.py)
Config:       2 files (config.py, .env)
Tests:        6 files
Docs:         8 files
Total Lines:  ~3,500+
```
