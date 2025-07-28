"""
Main database class for the personal document database.
Orchestrates all components and provides the public API.
"""

from typing import Any, Dict, List, Optional, Union
from docstore.document import Document
from docstore.storage import Storage
from docstore.query import QueryEngine
from docstore.index import IndexManager


class Database:
    """
    Main database class that provides document storage and querying capabilities.
    
    Features:
    - CRUD operations (Create, Read, Update, Delete)
    - Query language with comparison and logical operators
    - Indexing for fast lookups
    - Persistence to disk
    - Backup and restore functionality
    """
    
    def __init__(self, data_directory: str = "data"):
        """
        Initialize the database.
        
        Args:
            data_directory: Directory to store documents
        """
        self.storage = Storage(data_directory)
        self.query_engine = QueryEngine()
        self.index_manager = IndexManager()
        
        # Load existing documents and rebuild indexes
        self._load_documents()
    
    def _load_documents(self) -> None:
        """Load all documents from storage and rebuild indexes."""
        documents = self.storage.load_all_documents()
        self.index_manager.rebuild_indexes(documents)
    
    # CRUD Operations
    
    def insert(self, data: Dict[str, Any], document_id: Optional[str] = None) -> str:
        """
        Insert a new document.
        
        Args:
            data: Document data
            document_id: Optional custom ID
            
        Returns:
            ID of the inserted document
        """
        document = Document(data, document_id)
        
        # Check for unique constraint violations
        for field_path in self.index_manager.get_indexed_fields():
            if self.index_manager.indexes[field_path].unique:
                value = self._get_field_value(document, field_path)
                if value is not None:
                    existing_ids = self.index_manager.find_by_index(field_path, value)
                    if existing_ids:
                        raise ValueError(f"Unique constraint violated for field {field_path}")
        
        # Save to storage
        self.storage.save_document(document)
        
        # Add to indexes
        self.index_manager.add_document_to_indexes(document)
        
        return document.id
    
    def insert_many(self, documents_data: List[Dict[str, Any]]) -> List[str]:
        """
        Insert multiple documents.
        
        Args:
            documents_data: List of document data dictionaries
            
        Returns:
            List of inserted document IDs
        """
        document_ids = []
        
        for data in documents_data:
            doc_id = self.insert(data)
            document_ids.append(doc_id)
        
        return document_ids
    
    def find_by_id(self, document_id: str) -> Optional[Document]:
        """
        Find a document by ID.
        
        Args:
            document_id: ID of the document to find
            
        Returns:
            Document if found, None otherwise
        """
        return self.storage.load_document(document_id)
    
    def find(self, query: Dict[str, Any], limit: Optional[int] = None, skip: Optional[int] = None) -> List[Document]:
        """
        Find documents matching query criteria.
        
        Args:
            query: Query criteria
            limit: Maximum number of documents to return
            skip: Number of documents to skip
            
        Returns:
            List of matching documents
        """
        # Try to use indexes for simple queries
        indexed_ids = self._get_indexed_document_ids(query)
        
        if indexed_ids is not None:
            # Use index results
            documents = []
            for doc_id in indexed_ids:
                doc = self.find_by_id(doc_id)
                if doc and self.query_engine.match_document(doc, query):
                    documents.append(doc)
        else:
            # Load all documents and filter
            documents = self.storage.load_all_documents()
            documents = self.query_engine.filter_documents(documents, query)
        
        # Apply skip and limit
        if skip:
            documents = self.query_engine.skip_documents(documents, skip)
        if limit:
            documents = self.query_engine.limit_documents(documents, limit)
        
        return documents
    
    def find_one(self, query: Dict[str, Any]) -> Optional[Document]:
        """
        Find a single document matching query criteria.
        
        Args:
            query: Query criteria
            
        Returns:
            First matching document, or None if not found
        """
        results = self.find(query, limit=1)
        return results[0] if results else None
    
    def update(self, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        """
        Update documents matching query criteria.
        
        Args:
            query: Query criteria to match documents
            update_data: Data to update in matching documents
            
        Returns:
            Number of documents updated
        """
        documents = self.find(query)
        updated_count = 0
        
        for document in documents:
            # Remove from indexes
            self.index_manager.remove_document_from_indexes(document.id)
            
            # Update document
            document.update(update_data)
            
            # Save to storage
            self.storage.save_document(document)
            
            # Add back to indexes
            self.index_manager.add_document_to_indexes(document)
            
            updated_count += 1
        
        return updated_count
    
    def update_by_id(self, document_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update a specific document by ID.
        
        Args:
            document_id: ID of the document to update
            update_data: Data to update
            
        Returns:
            True if document was updated, False if not found
        """
        document = self.find_by_id(document_id)
        if not document:
            return False
        
        # Remove from indexes
        self.index_manager.remove_document_from_indexes(document.id)
        
        # Update document
        document.update(update_data)
        
        # Save to storage
        self.storage.save_document(document)
        
        # Add back to indexes
        self.index_manager.add_document_to_indexes(document)
        
        return True
    
    def upsert(self, query: Dict[str, Any], data: Dict[str, Any]) -> str:
        """
        Update a document if it exists, otherwise insert a new one.
        
        Args:
            query: Query criteria to find existing document
            data: Data for the document
            
        Returns:
            ID of the document (existing or new)
        """
        existing = self.find_one(query)
        if existing:
            self.update_by_id(existing.id, data)
            return existing.id
        else:
            return self.insert(data)
    
    def delete(self, query: Dict[str, Any]) -> int:
        """
        Delete documents matching query criteria.
        
        Args:
            query: Query criteria to match documents
            
        Returns:
            Number of documents deleted
        """
        documents = self.find(query)
        deleted_count = 0
        
        for document in documents:
            # Remove from indexes
            self.index_manager.remove_document_from_indexes(document.id)
            
            # Delete from storage
            if self.storage.delete_document(document.id):
                deleted_count += 1
        
        return deleted_count
    
    def delete_by_id(self, document_id: str) -> bool:
        """
        Delete a specific document by ID.
        
        Args:
            document_id: ID of the document to delete
            
        Returns:
            True if document was deleted, False if not found
        """
        # Remove from indexes
        self.index_manager.remove_document_from_indexes(document_id)
        
        # Delete from storage
        return self.storage.delete_document(document_id)
    
    def delete_all(self) -> int:
        """
        Delete all documents.
        
        Returns:
            Number of documents deleted
        """
        document_ids = self.storage.list_document_ids()
        deleted_count = len(document_ids)
        
        # Clear indexes
        for index in self.index_manager.indexes.values():
            index.value_to_ids.clear()
            index.id_to_value.clear()
        
        # Clear storage
        self.storage.clear_all()
        
        return deleted_count
    
    # Indexing Operations
    
    def create_index(self, field_path: str, unique: bool = False) -> None:
        """
        Create an index on a field.
        
        Args:
            field_path: Path to the field to index
            unique: Whether this index should enforce uniqueness
        """
        self.index_manager.create_index(field_path, unique)
        
        # Rebuild index with existing documents
        documents = self.storage.load_all_documents()
        for document in documents:
            self.index_manager.indexes[field_path].add_document(document)
    
    def drop_index(self, field_path: str) -> None:
        """
        Drop an index.
        
        Args:
            field_path: Path to the field to drop index from
        """
        self.index_manager.drop_index(field_path)
    
    def get_indexes(self) -> List[str]:
        """
        Get list of all indexed fields.
        
        Returns:
            List of indexed field paths
        """
        return self.index_manager.get_indexed_fields()
    
    def get_index_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Get statistics for all indexes.
        
        Returns:
            Dictionary with index statistics
        """
        return self.index_manager.get_index_stats()
    
    # Utility Methods
    
    def count(self, query: Optional[Dict[str, Any]] = None) -> int:
        """
        Count documents matching query criteria.
        
        Args:
            query: Query criteria (counts all documents if None)
            
        Returns:
            Number of matching documents
        """
        if query is None:
            return len(self.storage.list_document_ids())
        else:
            return len(self.find(query))
    
    def exists(self, query: Dict[str, Any]) -> bool:
        """
        Check if any documents match query criteria.
        
        Args:
            query: Query criteria
            
        Returns:
            True if any documents match, False otherwise
        """
        return self.find_one(query) is not None
    
    def distinct(self, field_path: str, query: Optional[Dict[str, Any]] = None) -> List[Any]:
        """
        Get distinct values for a field.
        
        Args:
            field_path: Path to the field
            query: Optional query to filter documents
            
        Returns:
            List of distinct values
        """
        documents = self.find(query) if query else self.storage.load_all_documents()
        distinct_values = set()
        
        for document in documents:
            value = self._get_field_value(document, field_path)
            if value is not None:
                distinct_values.add(value)
        
        return list(distinct_values)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary with database statistics
        """
        storage_info = self.storage.get_storage_info()
        index_stats = self.index_manager.get_index_stats()
        
        return {
            "storage": storage_info,
            "indexes": index_stats,
            "total_documents": storage_info["document_count"],
            "indexed_fields": len(index_stats)
        }
    
    def backup(self, backup_directory: str) -> None:
        """
        Create a backup of the database.
        
        Args:
            backup_directory: Directory to store backup
        """
        self.storage.backup_documents(backup_directory)
    
    def restore(self, backup_directory: str) -> None:
        """
        Restore database from backup.
        
        Args:
            backup_directory: Directory containing backup
        """
        self.storage.restore_documents(backup_directory)
        self._load_documents()
    
    def _get_indexed_document_ids(self, query: Dict[str, Any]) -> Optional[set]:
        """
        Try to use indexes to get document IDs for a query.
        
        Args:
            query: Query criteria
            
        Returns:
            Set of document IDs if indexes can be used, None otherwise
        """
        # Simple case: single field equality query
        if len(query) == 1:
            field_path, value = next(iter(query.items()))
            if not isinstance(value, dict) and self.index_manager.has_index(field_path):
                return self.index_manager.find_by_index(field_path, value)
        
        return None
    
    def _get_field_value(self, document: Document, field_path: str) -> Any:
        """
        Get a field value from a document using dot notation.
        
        Args:
            document: Document to extract value from
            field_path: Path to the field
            
        Returns:
            Value of the field, or None if not found
        """
        keys = field_path.split('.')
        current = document.data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return current 