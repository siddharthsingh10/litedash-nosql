"""
Document class for the personal document database.
Represents a single document with metadata and data.
"""

import json
import uuid
from datetime import datetime
from typing import Any, Dict, Optional


class Document:
    """
    Represents a document in the database.
    
    A document contains:
    - _id: Unique identifier
    - data: The actual document data
    - metadata: Creation/update timestamps and other metadata
    """
    
    def __init__(
        self, 
        data: Dict[str, Any], 
        document_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        Initialize a new document.
        
        Args:
            data: The document data (dict)
            document_id: Optional custom ID, auto-generated if not provided
            created_at: Creation timestamp, auto-generated if not provided
            updated_at: Update timestamp, auto-generated if not provided
        """
        self._id = document_id or str(uuid.uuid4())
        self.data = data
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @property
    def id(self) -> str:
        """Get the document ID."""
        return self._id
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert document to dictionary format for storage.
        
        Returns:
            Dictionary representation of the document
        """
        return {
            "_id": self._id,
            "data": self.data,
            "metadata": {
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()
            }
        }
    
    @classmethod
    def from_dict(cls, doc_dict: Dict[str, Any]) -> 'Document':
        """
        Create a document from dictionary format.
        
        Args:
            doc_dict: Dictionary representation of the document
            
        Returns:
            Document instance
        """
        document_id = doc_dict.get("_id")
        data = doc_dict.get("data", {})
        
        metadata = doc_dict.get("metadata", {})
        created_at_str = metadata.get("created_at")
        updated_at_str = metadata.get("updated_at")
        
        created_at = datetime.fromisoformat(created_at_str) if created_at_str else None
        updated_at = datetime.fromisoformat(updated_at_str) if updated_at_str else None
        
        return cls(data, document_id, created_at, updated_at)
    
    def update(self, new_data: Dict[str, Any]) -> None:
        """
        Update the document data.
        
        Args:
            new_data: New data to merge with existing data
        """
        self.data.update(new_data)
        self.updated_at = datetime.utcnow()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the document data.
        
        Args:
            key: Key to retrieve
            default: Default value if key doesn't exist
            
        Returns:
            Value associated with the key
        """
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the document data.
        
        Args:
            key: Key to set
            value: Value to set
        """
        self.data[key] = value
        self.updated_at = datetime.utcnow()
    
    def to_json(self) -> str:
        """
        Convert document to JSON string.
        
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Document':
        """
        Create document from JSON string.
        
        Args:
            json_str: JSON string representation
            
        Returns:
            Document instance
        """
        doc_dict = json.loads(json_str)
        return cls.from_dict(doc_dict)
    
    def __str__(self) -> str:
        """String representation of the document."""
        return f"Document(id={self._id}, data={self.data})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"Document(id='{self._id}', data={self.data}, created_at={self.created_at}, updated_at={self.updated_at})"
    
    def __eq__(self, other: Any) -> bool:
        """Check if two documents are equal."""
        if not isinstance(other, Document):
            return False
        return (
            self._id == other._id and
            self.data == other.data
        )
    
    def __hash__(self) -> int:
        """Hash of the document (based on ID)."""
        return hash(self._id) 