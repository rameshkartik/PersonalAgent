"""
Agent for communicating with the Vector DB Storage API.
Provides methods to fetch, search, and post information to/from the database.
"""
import httpx
from typing import List, Dict, Optional, Any
import json


class VectorDBAgent:
    """Agent for interacting with the Vector DB Storage API."""
    
    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 30.0):
        """
        Initialize the agent.
        
        Args:
            base_url: Base URL of the API server
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout)
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close the client."""
        self.close()
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()
    
    # ===== Health & Statistics =====
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if the API server is running.
        
        Returns:
            Health status information
        """
        response = self.client.get(f"{self.base_url}/")
        response.raise_for_status()
        return response.json()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get collection statistics.
        
        Returns:
            Statistics including total document count
        """
        response = self.client.get(f"{self.base_url}/stats")
        response.raise_for_status()
        return response.json()
    
    # ===== Create Operations =====
    
    def add_document(
        self,
        document: str,
        metadata: Optional[Dict[str, Any]] = None,
        doc_id: Optional[str] = None
    ) -> str:
        """
        Add a single document to the database.
        
        Args:
            document: The text content to store
            metadata: Optional metadata dictionary
            doc_id: Optional custom document ID
            
        Returns:
            The ID of the created document
            
        Example:
            >>> agent.add_document(
            ...     "I love hiking in the mountains",
            ...     metadata={"category": "hobbies", "type": "outdoor"}
            ... )
        """
        payload = {"document": document}
        if metadata:
            payload["metadata"] = metadata
        if doc_id:
            payload["id"] = doc_id
        
        response = self.client.post(
            f"{self.base_url}/documents",
            json=payload
        )
        response.raise_for_status()
        return response.json()["id"]
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add multiple documents to the database.
        
        Args:
            documents: List of text contents to store
            metadatas: Optional list of metadata dictionaries
            ids: Optional list of custom document IDs
            
        Returns:
            List of IDs of the created documents
            
        Example:
            >>> agent.add_documents(
            ...     documents=["I live in New York", "I love pizza"],
            ...     metadatas=[
            ...         {"category": "location", "type": "city"},
            ...         {"category": "food", "type": "preference"}
            ...     ]
            ... )
        """
        payload = {"documents": documents}
        if metadatas:
            payload["metadatas"] = metadatas
        if ids:
            payload["ids"] = ids
        
        response = self.client.post(
            f"{self.base_url}/documents/bulk",
            json=payload
        )
        response.raise_for_status()
        return response.json()["ids"]
    
    # ===== Read Operations =====
    
    def get_document(self, doc_id: str) -> Dict[str, Any]:
        """
        Get a specific document by ID.
        
        Args:
            doc_id: The document ID
            
        Returns:
            Document data including id, document text, and metadata
            
        Example:
            >>> doc = agent.get_document("abc-123")
            >>> print(doc["document"])
        """
        response = self.client.get(f"{self.base_url}/documents/{doc_id}")
        response.raise_for_status()
        return response.json()
    
    def get_all_documents(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all documents from the database.
        
        Args:
            limit: Optional limit on number of documents to return
            
        Returns:
            List of all documents
            
        Example:
            >>> docs = agent.get_all_documents(limit=10)
            >>> for doc in docs:
            ...     print(doc["document"])
        """
        url = f"{self.base_url}/documents"
        if limit:
            url += f"?limit={limit}"
        
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()
    
    # ===== Search Operations =====
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Search for documents using semantic similarity.
        
        Args:
            query: The search query text
            n_results: Number of results to return (1-100)
            where: Optional metadata filter
            
        Returns:
            Dictionary with ids, documents, metadatas, and distances
            
        Example:
            >>> results = agent.search("what is my name?", n_results=3)
            >>> for doc, score in zip(results["documents"], results["distances"]):
            ...     print(f"{doc} (score: {score})")
            
            >>> # Search with metadata filter
            >>> results = agent.search(
            ...     "personal information",
            ...     where={"category": "personal-info"}
            ... )
        """
        payload = {
            "query_text": query,
            "n_results": n_results
        }
        if where:
            payload["where"] = where
        
        response = self.client.post(
            f"{self.base_url}/query",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def ask(self, question: str, n_results: int = 3) -> str:
        """
        Ask a natural language question and get the most relevant answer.
        
        Args:
            question: The question to ask
            n_results: Number of documents to search
            
        Returns:
            The most relevant document text
            
        Example:
            >>> answer = agent.ask("where do I live?")
            >>> print(answer)
        """
        results = self.search(question, n_results=n_results)
        if results["documents"]:
            return results["documents"][0]
        return "No relevant information found."
    
    # ===== Update Operations =====
    
    def update_document(
        self,
        doc_id: str,
        document: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Update a document's content or metadata.
        
        Args:
            doc_id: The document ID to update
            document: Optional new document text
            metadata: Optional new metadata
            
        Returns:
            True if successful
            
        Example:
            >>> agent.update_document(
            ...     "abc-123",
            ...     metadata={"category": "updated", "verified": True}
            ... )
        """
        payload = {}
        if document is not None:
            payload["document"] = document
        if metadata is not None:
            payload["metadata"] = metadata
        
        response = self.client.put(
            f"{self.base_url}/documents/{doc_id}",
            json=payload
        )
        response.raise_for_status()
        return response.json()["success"]
    
    # ===== Delete Operations =====
    
    def delete_document(self, doc_id: str) -> bool:
        """
        Delete a document by ID.
        
        Args:
            doc_id: The document ID to delete
            
        Returns:
            True if successful
            
        Example:
            >>> agent.delete_document("abc-123")
        """
        response = self.client.delete(f"{self.base_url}/documents/{doc_id}")
        response.raise_for_status()
        return response.json()["success"]
    
    def reset_collection(self) -> bool:
        """
        Delete ALL documents from the collection.
        
        WARNING: This action cannot be undone!
        
        Returns:
            True if successful
        """
        response = self.client.delete(f"{self.base_url}/reset")
        response.raise_for_status()
        return response.json()["success"]
    
    # ===== Convenience Methods =====
    
    def add_from_dict(self, data: Dict[str, Any]) -> str:
        """
        Add a document from a dictionary containing 'document' and optionally 'metadata'.
        
        Args:
            data: Dictionary with 'document' key and optional 'metadata', 'id'
            
        Returns:
            The ID of the created document
        """
        return self.add_document(
            document=data["document"],
            metadata=data.get("metadata"),
            doc_id=data.get("id")
        )
    
    def add_from_file(self, filepath: str) -> List[str]:
        """
        Add documents from a JSON file (bulk insert format).
        
        Args:
            filepath: Path to JSON file with 'documents' and 'metadatas' keys
            
        Returns:
            List of created document IDs
            
        Example:
            >>> agent.add_from_file("BulkInsert.json")
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return self.add_documents(
            documents=data["documents"],
            metadatas=data.get("metadatas"),
            ids=data.get("ids")
        )
    
    def find_by_metadata(
        self,
        category: Optional[str] = None,
        **filters
    ) -> List[Dict[str, Any]]:
        """
        Find documents by metadata fields.
        
        Args:
            category: Optional category filter
            **filters: Additional metadata key-value filters
            
        Returns:
            List of matching documents
            
        Example:
            >>> docs = agent.find_by_metadata(category="personal-info")
            >>> docs = agent.find_by_metadata(category="work", type="role")
        """
        where = {}
        if category:
            where["category"] = category
        where.update(filters)
        
        # Search with a generic query and metadata filter
        results = self.search(
            query="documents",
            n_results=100,
            where=where if where else None
        )
        
        # Convert to document list format
        documents = []
        for i in range(len(results["ids"])):
            documents.append({
                "id": results["ids"][i],
                "document": results["documents"][i],
                "metadata": results["metadatas"][i]
            })
        
        return documents
    
    def print_search_results(self, results: Dict[str, Any]):
        """
        Pretty print search results.
        
        Args:
            results: Search results from search() method
        """
        print(f"\nFound {len(results['ids'])} results:\n")
        for i, (doc_id, doc, meta, dist) in enumerate(zip(
            results["ids"],
            results["documents"],
            results["metadatas"],
            results["distances"]
        ), 1):
            print(f"{i}. {doc}")
            print(f"   ID: {doc_id}")
            print(f"   Score: {dist:.4f}")
            if meta:
                print(f"   Metadata: {meta}")
            print()


# ===== Example Usage =====

if __name__ == "__main__":
    # Create agent
    with VectorDBAgent() as agent:
        # Health check
        print("Checking API health...")
        health = agent.health_check()
        print(f"API Status: {health['status']}\n")
        
        # Get statistics
        stats = agent.get_stats()
        print(f"Total documents: {stats['total_documents']}\n")
        
        # Search for information
        print("Searching: 'what is my name?'")
        results = agent.search("what is my name?", n_results=3)
        agent.print_search_results(results)
        
        # Ask a question
        print("Asking: 'where do I live?'")
        answer = agent.ask("where do I live?")
        print(f"Answer: {answer}\n")
        
        # Get all documents
        print("All documents:")
        all_docs = agent.get_all_documents(limit=5)
        for doc in all_docs:
            print(f"  - {doc['document'][:60]}...")
        print()
