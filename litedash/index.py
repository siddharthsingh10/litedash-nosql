"""
Indexing system for the personal document database.
Provides fast lookups for frequently queried fields.
"""

from typing import Any, Dict, List, Optional, Set
from collections import defaultdict
from litedash.document import Document


class Index:
    """
    Represents an index on a specific field.
    
    Maintains a mapping from field values to document IDs for fast lookups.
    """
    
    def __init__(self, field_path: str, unique: bool = False):
        """
        Initialize an index.
        
        Args:
            field_path: Path to the indexed field (supports dot notation)
            unique: Whether this index enforces uniqueness
        """
        self.field_path = field_path
        self.unique = unique
        self.value_to_ids: Dict[Any, Set[str]] = defaultdict(set)
        self.id_to_value: Dict[str, Any] = {}
    
    def add_document(self, document: Document) -> None:
        """
        Add a document to the index.
        
        Args:
            document: Document to index
        """
        value = self._get_field_value(document)
        doc_id = document.id
        
        # Remove old value if document was already indexed
        if doc_id in self.id_to_value:
            old_value = self.id_to_value[doc_id]
            self.value_to_ids[old_value].discard(doc_id)
            if not self.value_to_ids[old_value]:
                del self.value_to_ids[old_value]
        
        # Add new value
        if value is not None:
            self.value_to_ids[value].add(doc_id)
            self.id_to_value[doc_id] = value
            
            # Check uniqueness constraint
            if self.unique and len(self.value_to_ids[value]) > 1:
                raise ValueError(f"Unique constraint violated for field {self.field_path}")
    
    def remove_document(self, document_id: str) -> None:
        """
        Remove a document from the index.
        
        Args:
            document_id: ID of the document to remove
        """
        if document_id in self.id_to_value:
            value = self.id_to_value[document_id]
            self.value_to_ids[value].discard(document_id)
            if not self.value_to_ids[value]:
                del self.value_to_ids[value]
            del self.id_to_value[document_id]
    
    def find_by_value(self, value: Any) -> Set[str]:
        """
        Find document IDs by field value.
        
        Args:
            value: Value to search for
            
        Returns:
            Set of document IDs that match the value
        """
        return self.value_to_ids.get(value, set()).copy()
    
    def find_by_range(self, min_value: Any = None, max_value: Any = None) -> Set[str]:
        """
        Find document IDs within a range.
        
        Args:
            min_value: Minimum value (inclusive)
            max_value: Maximum value (inclusive)
            
        Returns:
            Set of document IDs within the range
        """
        result = set()
        
        for value, doc_ids in self.value_to_ids.items():
            if value is None:
                continue
                
            if min_value is not None and value < min_value:
                continue
            if max_value is not None and value > max_value:
                continue
                
            result.update(doc_ids)
        
        return result
    
    def get_all_values(self) -> List[Any]:
        """
        Get all unique values in the index.
        
        Returns:
            List of unique values
        """
        return list(self.value_to_ids.keys())
    
    def get_index_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the index.
        
        Returns:
            Dictionary with index statistics
        """
        total_documents = len(self.id_to_value)
        unique_values = len(self.value_to_ids)
        
        return {
            "field_path": self.field_path,
            "unique": self.unique,
            "total_documents": total_documents,
            "unique_values": unique_values,
            "average_documents_per_value": total_documents / unique_values if unique_values > 0 else 0
        }
    
    def _get_field_value(self, document: Document) -> Any:
        """
        Extract the field value from a document.
        
        Args:
            document: Document to extract value from
            
        Returns:
            Value of the indexed field
        """
        keys = self.field_path.split('.')
        current = document.data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return current


class IndexManager:
    """
    Manages multiple indexes for the database.
    """
    
    def __init__(self):
        """Initialize the index manager."""
        self.indexes: Dict[str, Index] = {}
    
    def create_index(self, field_path: str, unique: bool = False) -> None:
        """
        Create a new index.
        
        Args:
            field_path: Path to the field to index
            unique: Whether this index should enforce uniqueness
        """
        if field_path in self.indexes:
            raise ValueError(f"Index on field {field_path} already exists")
        
        self.indexes[field_path] = Index(field_path, unique)
    
    def drop_index(self, field_path: str) -> None:
        """
        Drop an index.
        
        Args:
            field_path: Path to the field to drop index from
        """
        if field_path in self.indexes:
            del self.indexes[field_path]
    
    def add_document_to_indexes(self, document: Document) -> None:
        """
        Add a document to all indexes.
        
        Args:
            document: Document to add to indexes
        """
        for index in self.indexes.values():
            index.add_document(document)
    
    def remove_document_from_indexes(self, document_id: str) -> None:
        """
        Remove a document from all indexes.
        
        Args:
            document_id: ID of the document to remove
        """
        for index in self.indexes.values():
            index.remove_document(document_id)
    
    def find_by_index(self, field_path: str, value: Any) -> Set[str]:
        """
        Find documents using an index.
        
        Args:
            field_path: Path to the indexed field
            value: Value to search for
            
        Returns:
            Set of document IDs that match
        """
        if field_path not in self.indexes:
            return set()
        
        return self.indexes[field_path].find_by_value(value)
    
    def find_by_index_range(self, field_path: str, min_value: Any = None, max_value: Any = None) -> Set[str]:
        """
        Find documents using an index within a range.
        
        Args:
            field_path: Path to the indexed field
            min_value: Minimum value (inclusive)
            max_value: Maximum value (inclusive)
            
        Returns:
            Set of document IDs within the range
        """
        if field_path not in self.indexes:
            return set()
        
        return self.indexes[field_path].find_by_range(min_value, max_value)
    
    def get_indexed_fields(self) -> List[str]:
        """
        Get list of all indexed fields.
        
        Returns:
            List of field paths that have indexes
        """
        return list(self.indexes.keys())
    
    def get_index_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Get statistics for all indexes.
        
        Returns:
            Dictionary mapping field paths to index statistics
        """
        return {
            field_path: index.get_index_stats()
            for field_path, index in self.indexes.items()
        }
    
    def rebuild_indexes(self, documents: List[Document]) -> None:
        """
        Rebuild all indexes from scratch.
        
        Args:
            documents: List of all documents to index
        """
        # Clear all indexes
        for index in self.indexes.values():
            index.value_to_ids.clear()
            index.id_to_value.clear()
        
        # Rebuild indexes
        for document in documents:
            self.add_document_to_indexes(document)
    
    def has_index(self, field_path: str) -> bool:
        """
        Check if a field has an index.
        
        Args:
            field_path: Path to the field
            
        Returns:
            True if field has an index, False otherwise
        """
        return field_path in self.indexes 