"""
FastAPI External API for Vector DB Storage Layer
Provides REST endpoints to interact with the Vector DB storage.
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from storage import get_storage
from models import (
    DocumentCreate, DocumentsCreate, DocumentUpdate, QueryRequest,
    DocumentResponse, QueryResponse, DocumentCreateResponse,
    DocumentsCreateResponse, SuccessResponse, ErrorResponse, StatsResponse
)
from config import config


# Initialize FastAPI app
app = FastAPI(
    title="Vector DB Storage API",
    description="External API for managing personal information in Vector Database",
    version="1.0.0"
)

# Add CORS middleware to allow web app access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Vector DB Storage API is running",
        "version": "1.0.0"
    }


@app.get("/stats", response_model=StatsResponse, tags=["Statistics"])
async def get_stats():
    """Get collection statistics."""
    storage = get_storage()
    return StatsResponse(
        total_documents=storage.count_documents(),
        collection_name=config.COLLECTION_NAME
    )


@app.post(
    "/documents",
    response_model=DocumentCreateResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Documents"]
)
async def create_document(doc: DocumentCreate):
    """
    Add a new document to the storage.
    
    - **document**: The text content to store
    - **metadata**: Optional metadata (key-value pairs)
    - **id**: Optional custom ID (auto-generated if not provided)
    """
    try:
        storage = get_storage()
        doc_id = storage.add_document(
            document=doc.document,
            metadata=doc.metadata,
            doc_id=doc.id
        )
        return DocumentCreateResponse(
            id=doc_id,
            message="Document created successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create document: {str(e)}"
        )


@app.post(
    "/documents/bulk",
    response_model=DocumentsCreateResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Documents"]
)
async def create_documents(docs: DocumentsCreate):
    """
    Add multiple documents to the storage.
    
    - **documents**: List of text contents to store
    - **metadatas**: Optional list of metadata dictionaries
    - **ids**: Optional list of custom IDs
    """
    try:
        storage = get_storage()
        doc_ids = storage.add_documents(
            documents=docs.documents,
            metadatas=docs.metadatas,
            ids=docs.ids
        )
        return DocumentsCreateResponse(
            ids=doc_ids,
            message="Documents created successfully",
            count=len(doc_ids)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create documents: {str(e)}"
        )


@app.get("/documents/{doc_id}", response_model=DocumentResponse, tags=["Documents"])
async def get_document(doc_id: str):
    """
    Get a document by ID.
    
    - **doc_id**: The document ID
    """
    storage = get_storage()
    document = storage.get_document(doc_id)
    
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID '{doc_id}' not found"
        )
    
    return DocumentResponse(**document)


@app.get("/documents", response_model=List[DocumentResponse], tags=["Documents"])
async def get_all_documents(limit: int = None):
    """
    Get all documents in the collection.
    
    - **limit**: Optional limit on number of documents to return
    """
    storage = get_storage()
    documents = storage.get_all_documents(limit=limit)
    return [DocumentResponse(**doc) for doc in documents]


@app.put("/documents/{doc_id}", response_model=SuccessResponse, tags=["Documents"])
async def update_document(doc_id: str, update: DocumentUpdate):
    """
    Update a document.
    
    - **doc_id**: The document ID
    - **document**: Optional new document text
    - **metadata**: Optional new metadata
    """
    storage = get_storage()
    
    # Check if document exists
    if storage.get_document(doc_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID '{doc_id}' not found"
        )
    
    success = storage.update_document(
        doc_id=doc_id,
        document=update.document,
        metadata=update.metadata
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update document"
        )
    
    return SuccessResponse(success=True, message="Document updated successfully")


@app.delete("/documents/{doc_id}", response_model=SuccessResponse, tags=["Documents"])
async def delete_document(doc_id: str):
    """
    Delete a document by ID.
    
    - **doc_id**: The document ID
    """
    storage = get_storage()
    
    # Check if document exists
    if storage.get_document(doc_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID '{doc_id}' not found"
        )
    
    success = storage.delete_document(doc_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete document"
        )
    
    return SuccessResponse(success=True, message="Document deleted successfully")


@app.post("/query", response_model=QueryResponse, tags=["Search"])
async def query_documents(query: QueryRequest):
    """
    Query documents by similarity search.
    
    - **query_text**: The text to search for
    - **n_results**: Number of similar documents to return (1-100)
    - **where**: Optional metadata filter
    """
    try:
        storage = get_storage()
        results = storage.query_documents(
            query_text=query.query_text,
            n_results=query.n_results,
            where=query.where
        )
        return QueryResponse(**results)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query failed: {str(e)}"
        )


@app.delete("/reset", response_model=SuccessResponse, tags=["Management"])
async def reset_collection():
    """
    Delete all documents from the collection.
    
    WARNING: This action cannot be undone!
    """
    storage = get_storage()
    success = storage.reset_collection()
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset collection"
        )
    
    return SuccessResponse(success=True, message="Collection reset successfully")


# ===== LLM Agent Endpoints =====

from pydantic import BaseModel

class LLMChatRequest(BaseModel):
    """Request model for LLM chat."""
    message: str
    n_results: int = 3

class LLMChatResponse(BaseModel):
    """Response model for LLM chat."""
    response: str
    sources: List[str] = []

@app.post("/llm/chat", response_model=LLMChatResponse, tags=["LLM Agent"])
async def llm_chat(request: LLMChatRequest):
    """
    Chat with LLM agent - get intelligent responses based on stored information.
    
    The LLM agent will:
    1. Search the vector database for relevant information
    2. Use LLM to generate a natural, intelligent response
    
    Requires LLM configuration (OPENAI_API_KEY or other provider).
    """
    try:
        import openai
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        
        # Get LLM configuration
        llm_provider = os.getenv('LLM_PROVIDER', 'openai').lower()
        
        # Initialize OpenAI client
        if llm_provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set in .env file")
            llm_client = openai.OpenAI(api_key=api_key)
            model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")
        
        # Search for relevant context using storage directly (no HTTP calls)
        storage = get_storage()
        results = storage.query_documents(request.message, n_results=request.n_results)
        
        # Build context
        if results["documents"]:
            context = "\n".join(f"- {doc}" for doc in results["documents"])
            context_message = f"\nRelevant information from knowledge base:\n{context}"
        else:
            context_message = "\nNo relevant information found in knowledge base."
        
        # Build LLM messages
        messages = [
            {"role": "system", "content": "You are a personal information retrieval assistant. Your job is to retrieve and share information from the user's PERSONAL knowledge base. This is the user's own data that they have stored. Always provide the requested information directly from the context provided - do NOT refuse to share personal details like IDs, numbers, or addresses since this is the user retrieving their OWN information. Be direct and factual."},
            {"role": "user", "content": request.message + context_message}
        ]
        
        # Get LLM response
        response = llm_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            timeout=30.0
        )
        
        llm_response = response.choices[0].message.content
        
        return LLMChatResponse(
            response=llm_response,
            sources=results["documents"][:3]  # Return top 3 sources
        )
        
    except ImportError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM dependencies not installed: {str(e)}. Install with: pip install openai"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM configuration error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing LLM request: {str(e)}"
        )


@app.post("/llm/smart-ask", response_model=LLMChatResponse, tags=["LLM Agent"])
async def llm_smart_ask(request: LLMChatRequest):
    """
    Ask a question and get an LLM-generated intelligent response.
    
    Similar to chat but for single questions without conversation history.
    """
    try:
        import openai
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        
        # Get LLM configuration
        llm_provider = os.getenv('LLM_PROVIDER', 'openai').lower()
        
        # Initialize OpenAI client
        if llm_provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY not set in .env file")
            llm_client = openai.OpenAI(api_key=api_key)
            model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")
        
        # Search for relevant context using storage directly
        storage = get_storage()
        results = storage.query_documents(request.message, n_results=request.n_results)
        
        # Build context with sources
        if results["documents"]:
            context_parts = []
            for i, doc in enumerate(results["documents"], 1):
                context_parts.append(f"{i}. {doc}")
            context = "\n".join(context_parts)
            context_message = f"\n\nRelevant information from knowledge base:\n{context}\n\nBased on this information, please answer the question."
        else:
            context_message = "\n\nNo relevant information found in knowledge base. Please answer based on general knowledge if possible."
        
        # Build LLM messages
        messages = [
            {"role": "system", "content": "You are a personal information retrieval assistant. Your job is to retrieve and share information from the user's PERSONAL knowledge base. This is the user's own data that they have stored. Always provide the requested information directly from the context provided - do NOT refuse to share personal details like IDs, numbers, or addresses since this is the user retrieving their OWN information. Be direct and factual."},
            {"role": "user", "content": request.message + context_message}
        ]
        
        # Get LLM response
        response = llm_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            timeout=30.0
        )
        
        llm_response = response.choices[0].message.content
        
        return LLMChatResponse(
            response=llm_response,
            sources=results["documents"][:3]
        )
        
    except ImportError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM dependencies not installed: {str(e)}. Install with: pip install openai"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM configuration error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing LLM request: {str(e)}"
        )
        
        return LLMChatResponse(
            response=response,
            sources=sources[:3]
        )
        
    except ImportError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM dependencies not installed: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM configuration error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing LLM request: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.API_RELOAD
    )
