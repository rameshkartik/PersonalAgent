"""
Vector DB Storage Layer (Qdrant)
Handles all interactions with the Qdrant vector database.
"""
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, 
    VectorParams, 
    PointStruct, 
    Filter, 
    FieldCondition, 
    MatchValue,
    SearchRequest
)
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional, Any
import uuid
from config import config


class VectorDBStorage:
    """Storage layer for managing Qdrant vector database operations."""
    
    def __init__(self):
        """Initialize Qdrant client and collection."""
        # Initialize client with local persistence
        self.client = QdrantClient(path=config.VECTOR_DB_PATH)
        
        # Initialize embedding model
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.vector_size = 384  # all-MiniLM-L6-v2 produces 384-dimensional vectors
        
        # Create collection if it doesn't exist
        try:
            self.client.get_collection(config.COLLECTION_NAME)
        except:
            self.client.create_collection(
                collection_name=config.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )
    
    def _encode(self, text: str) -> List[float]:
        """Encode text to vector."""
        return self.encoder.encode(text).tolist()
    
    def add_document(
        self, 
        document: str, 
        metadata: Optional[Dict[str, Any]] = None,
        doc_id: Optional[str] = None
    ) -> str:
        """
        Add a document to the collection.
        
        Args:
            document: The text content to store
            metadata: Optional metadata associated with the document
            doc_id: Optional custom ID, auto-generated if not provided
            
        Returns:
            The ID of the added document
        """
        if doc_id is None:
            doc_id = str(uuid.uuid4())
        
        if metadata is None:
            metadata = {}
        
        # Add document text to metadata for retrieval
        payload = {**metadata, "document": document}
        
        vector = self._encode(document)
        
        self.client.upsert(
            collection_name=config.COLLECTION_NAME,
            points=[PointStruct(
                id=doc_id,
                vector=vector,
                payload=payload
            )]
        )
        
        return doc_id
    
    def add_documents(
        self, 
        documents: List[str], 
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add multiple documents to the collection.
        
        Args:
            documents: List of text contents to store
            metadatas: Optional list of metadata dictionaries
            ids: Optional list of custom IDs, auto-generated if not provided
            
        Returns:
            List of IDs of the added documents
        """
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in documents]
        
        if metadatas is None:
            metadatas = [{} for _ in documents]
        
        points = []
        for doc_id, document, metadata in zip(ids, documents, metadatas):
            payload = {**metadata, "document": document}
            vector = self._encode(document)
            points.append(PointStruct(
                id=doc_id,
                vector=vector,
                payload=payload
            ))
        
        self.client.upsert(
            collection_name=config.COLLECTION_NAME,
            points=points
        )
        
        return ids
    
    def query_documents(
        self, 
        query_text: str, 
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query documents by similarity.
        
        Args:
            query_text: The query text to search for
            n_results: Number of results to return
            where: Optional metadata filter
            
        Returns:
            Dictionary containing query results
        """
        query_vector = self._encode(query_text)
        
        # Build filter if provided
        query_filter = None
        if where:
            must_conditions = []
            for key, value in where.items():
                must_conditions.append(
                    FieldCondition(key=key, match=MatchValue(value=value))
                )
            if must_conditions:
                query_filter = Filter(must=must_conditions)
        
        # Use search API (compatible with qdrant-client 1.7.3)
        search_results = self.client.search(
            collection_name=config.COLLECTION_NAME,
            query_vector=query_vector,
            limit=n_results,
            query_filter=query_filter
        )
        
        ids = []
        documents = []
        metadatas = []
        distances = []
        
        for hit in search_results:
            ids.append(str(hit.id))
            payload = hit.payload
            documents.append(payload.get("document", ""))
            # Remove document from metadata
            metadata = {k: v for k, v in payload.items() if k != "document"}
            metadatas.append(metadata)
            distances.append(hit.score)
        
        return {
            "ids": ids,
            "documents": documents,
            "metadatas": metadatas,
            "distances": distances
        }
    
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a document by ID.
        
        Args:
            doc_id: The document ID
            
        Returns:
            Document data or None if not found
        """
        try:
            result = self.client.retrieve(
                collection_name=config.COLLECTION_NAME,
                ids=[doc_id]
            )
            
            if result:
                point = result[0]
                payload = point.payload
                return {
                    "id": str(point.id),
                    "document": payload.get("document", ""),
                    "metadata": {k: v for k, v in payload.items() if k != "document"}
                }
            return None
        except Exception:
            return None
    
    def update_document(
        self, 
        doc_id: str, 
        document: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Update a document.
        
        Args:
            doc_id: The document ID
            document: Optional new document text
            metadata: Optional new metadata
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get existing document
            existing = self.get_document(doc_id)
            if existing is None:
                return False
            
            # Prepare new payload
            new_document = document if document is not None else existing["document"]
            new_metadata = metadata if metadata is not None else existing["metadata"]
            
            # Update
            payload = {**new_metadata, "document": new_document}
            vector = self._encode(new_document)
            
            self.client.upsert(
                collection_name=config.COLLECTION_NAME,
                points=[PointStruct(
                    id=doc_id,
                    vector=vector,
                    payload=payload
                )]
            )
            return True
        except Exception:
            return False
    
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document by ID.
        
        Args:
            doc_id: The document ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.delete(
                collection_name=config.COLLECTION_NAME,
                points_selector=[doc_id]
            )
            return True
        except Exception:
            return False
    
    def delete_documents(self, where: Dict[str, Any]) -> bool:
        """
        Delete documents matching metadata filter.
        
        Args:
            where: Metadata filter
            
        Returns:
            True if successful, False otherwise
        """
        try:
            must_conditions = []
            for key, value in where.items():
                must_conditions.append(
                    FieldCondition(key=key, match=MatchValue(value=value))
                )
            
            if must_conditions:
                self.client.delete(
                    collection_name=config.COLLECTION_NAME,
                    points_selector=Filter(must=must_conditions)
                )
            return True
        except Exception:
            return False
    
    def get_all_documents(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all documents in the collection.
        
        Args:
            limit: Optional limit on number of documents
            
        Returns:
            List of all documents
        """
        # Scroll through all points
        points, _ = self.client.scroll(
            collection_name=config.COLLECTION_NAME,
            limit=limit if limit else 10000
        )
        
        documents = []
        for point in points:
            payload = point.payload
            documents.append({
                "id": str(point.id),
                "document": payload.get("document", ""),
                "metadata": {k: v for k, v in payload.items() if k != "document"}
            })
        
        return documents
    
    def count_documents(self) -> int:
        """
        Get the total number of documents in the collection.
        
        Returns:
            Number of documents
        """
        collection_info = self.client.get_collection(config.COLLECTION_NAME)
        return collection_info.points_count
    
    def reset_collection(self) -> bool:
        """
        Delete all documents from the collection.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.delete_collection(config.COLLECTION_NAME)
            self.client.create_collection(
                collection_name=config.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE
                )
            )
            return True
        except Exception:
            return False


# Singleton instance
_storage_instance = None


def get_storage() -> VectorDBStorage:
    """Get or create the Vector DB storage instance."""
    global _storage_instance
    if _storage_instance is None:
        _storage_instance = VectorDBStorage()
    return _storage_instance
