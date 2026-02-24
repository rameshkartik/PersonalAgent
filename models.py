"""
Pydantic models for API request and response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class DocumentCreate(BaseModel):
    """Model for creating a new document."""
    document: str = Field(..., description="The text content to store")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Optional metadata")
    id: Optional[str] = Field(default=None, description="Optional custom ID")


class DocumentsCreate(BaseModel):
    """Model for creating multiple documents."""
    documents: List[str] = Field(..., description="List of text contents to store")
    metadatas: Optional[List[Dict[str, Any]]] = Field(default=None, description="Optional list of metadata")
    ids: Optional[List[str]] = Field(default=None, description="Optional list of custom IDs")


class DocumentUpdate(BaseModel):
    """Model for updating a document."""
    document: Optional[str] = Field(default=None, description="New document text")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="New metadata")


class QueryRequest(BaseModel):
    """Model for querying documents."""
    query_text: str = Field(..., description="The query text to search for")
    n_results: int = Field(default=5, ge=1, le=100, description="Number of results to return")
    where: Optional[Dict[str, Any]] = Field(default=None, description="Optional metadata filter")


class DocumentResponse(BaseModel):
    """Model for document response."""
    id: str
    document: str
    metadata: Dict[str, Any]


class QueryResponse(BaseModel):
    """Model for query response."""
    ids: List[str]
    documents: List[str]
    metadatas: List[Dict[str, Any]]
    distances: List[float]


class DocumentCreateResponse(BaseModel):
    """Model for document creation response."""
    id: str
    message: str


class DocumentsCreateResponse(BaseModel):
    """Model for multiple documents creation response."""
    ids: List[str]
    message: str
    count: int


class SuccessResponse(BaseModel):
    """Model for success response."""
    success: bool
    message: str


class ErrorResponse(BaseModel):
    """Model for error response."""
    error: str
    detail: Optional[str] = None


class StatsResponse(BaseModel):
    """Model for collection statistics response."""
    total_documents: int
    collection_name: str
