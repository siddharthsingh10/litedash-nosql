"""
Unit tests for the Personal Document Database.
"""

import pytest
import tempfile
import shutil
import os
from datetime import datetime

# Add docstore to path for imports
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from docstore.database import Database
from docstore.document import Document


class TestDatabase:
    """Test cases for the Database class."""
    
    def setup_method(self):
        """Set up test environment before each test."""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.db = Database(self.test_dir)
    
    def teardown_method(self):
        """Clean up after each test."""
        # Remove temporary directory
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_insert_document(self):
        """Test inserting a single document."""
        data = {"name": "Test User", "email": "test@example.com"}
        doc_id = self.db.insert(data)
        
        assert doc_id is not None
        assert len(doc_id) > 0
        
        # Verify document was saved
        doc = self.db.find_by_id(doc_id)
        assert doc is not None
        assert doc.data["name"] == "Test User"
        assert doc.data["email"] == "test@example.com"
    
    def test_insert_many_documents(self):
        """Test inserting multiple documents."""
        documents = [
            {"name": "User 1", "age": 25},
            {"name": "User 2", "age": 30},
            {"name": "User 3", "age": 35}
        ]
        
        doc_ids = self.db.insert_many(documents)
        
        assert len(doc_ids) == 3
        assert all(len(doc_id) > 0 for doc_id in doc_ids)
        
        # Verify all documents were saved
        for doc_id in doc_ids:
            doc = self.db.find_by_id(doc_id)
            assert doc is not None
    
    def test_find_by_id(self):
        """Test finding document by ID."""
        data = {"name": "Test User", "email": "test@example.com"}
        doc_id = self.db.insert(data)
        
        doc = self.db.find_by_id(doc_id)
        assert doc is not None
        assert doc.id == doc_id
        assert doc.data == data
    
    def test_find_by_id_not_found(self):
        """Test finding non-existent document by ID."""
        doc = self.db.find_by_id("non-existent-id")
        assert doc is None
    
    def test_find_all_documents(self):
        """Test finding all documents."""
        # Insert multiple documents
        self.db.insert({"name": "User 1"})
        self.db.insert({"name": "User 2"})
        self.db.insert({"name": "User 3"})
        
        docs = self.db.find({})
        assert len(docs) == 3
    
    def test_find_with_query(self):
        """Test finding documents with query."""
        # Insert test data
        self.db.insert({"name": "Alice", "age": 25, "city": "NYC"})
        self.db.insert({"name": "Bob", "age": 30, "city": "SF"})
        self.db.insert({"name": "Charlie", "age": 35, "city": "NYC"})
        
        # Test simple equality
        nyc_users = self.db.find({"city": "NYC"})
        assert len(nyc_users) == 2
        
        # Test comparison operators
        young_users = self.db.find({"age": {"$lt": 30}})
        assert len(young_users) == 1
        
        old_users = self.db.find({"age": {"$gte": 30}})
        assert len(old_users) == 2
    
    def test_find_one(self):
        """Test finding single document."""
        self.db.insert({"name": "Alice", "email": "alice@example.com"})
        self.db.insert({"name": "Bob", "email": "bob@example.com"})
        
        doc = self.db.find_one({"name": "Alice"})
        assert doc is not None
        assert doc.data["name"] == "Alice"
        
        # Test not found
        doc = self.db.find_one({"name": "Charlie"})
        assert doc is None
    
    def test_update_by_id(self):
        """Test updating document by ID."""
        data = {"name": "Test User", "age": 25}
        doc_id = self.db.insert(data)
        
        # Update the document
        success = self.db.update_by_id(doc_id, {"age": 26})
        assert success is True
        
        # Verify update
        doc = self.db.find_by_id(doc_id)
        assert doc.data["age"] == 26
        assert doc.data["name"] == "Test User"  # Should remain unchanged
    
    def test_update_by_query(self):
        """Test updating documents with query."""
        # Insert test data
        self.db.insert({"name": "Alice", "age": 25, "city": "NYC"})
        self.db.insert({"name": "Bob", "age": 30, "city": "SF"})
        self.db.insert({"name": "Charlie", "age": 35, "city": "NYC"})
        
        # Update all NYC users
        updated_count = self.db.update({"city": "NYC"}, {"status": "active"})
        assert updated_count == 2
        
        # Verify updates
        nyc_users = self.db.find({"city": "NYC"})
        for user in nyc_users:
            assert user.data["status"] == "active"
    
    def test_upsert(self):
        """Test upsert functionality."""
        # Insert new document
        doc_id = self.db.upsert(
            {"email": "test@example.com"},
            {"name": "Test User", "email": "test@example.com", "age": 25}
        )
        assert doc_id is not None
        
        # Update existing document
        updated_id = self.db.upsert(
            {"email": "test@example.com"},
            {"name": "Updated User", "email": "test@example.com", "age": 26}
        )
        assert updated_id == doc_id
        
        # Verify update
        doc = self.db.find_by_id(doc_id)
        assert doc.data["name"] == "Updated User"
        assert doc.data["age"] == 26
    
    def test_delete_by_id(self):
        """Test deleting document by ID."""
        doc_id = self.db.insert({"name": "Test User"})
        
        # Delete the document
        success = self.db.delete_by_id(doc_id)
        assert success is True
        
        # Verify deletion
        doc = self.db.find_by_id(doc_id)
        assert doc is None
    
    def test_delete_by_query(self):
        """Test deleting documents with query."""
        # Insert test data
        self.db.insert({"name": "Alice", "city": "NYC"})
        self.db.insert({"name": "Bob", "city": "SF"})
        self.db.insert({"name": "Charlie", "city": "NYC"})
        
        # Delete all NYC users
        deleted_count = self.db.delete({"city": "NYC"})
        assert deleted_count == 2
        
        # Verify deletion
        remaining = self.db.find({})
        assert len(remaining) == 1
        assert remaining[0].data["name"] == "Bob"
    
    def test_delete_all(self):
        """Test deleting all documents."""
        # Insert test data
        self.db.insert({"name": "User 1"})
        self.db.insert({"name": "User 2"})
        self.db.insert({"name": "User 3"})
        
        # Delete all
        deleted_count = self.db.delete_all()
        assert deleted_count == 3
        
        # Verify all deleted
        remaining = self.db.find({})
        assert len(remaining) == 0
    
    def test_count(self):
        """Test counting documents."""
        # Insert test data
        self.db.insert({"name": "User 1"})
        self.db.insert({"name": "User 2"})
        self.db.insert({"name": "User 3"})
        
        # Count all
        total = self.db.count()
        assert total == 3
        
        # Count with query
        count = self.db.count({"name": "User 1"})
        assert count == 1
    
    def test_exists(self):
        """Test checking document existence."""
        self.db.insert({"name": "Test User", "email": "test@example.com"})
        
        # Check existing
        exists = self.db.exists({"name": "Test User"})
        assert exists is True
        
        # Check non-existing
        exists = self.db.exists({"name": "Non-existent"})
        assert exists is False
    
    def test_distinct(self):
        """Test getting distinct values."""
        # Insert test data
        self.db.insert({"name": "Alice", "city": "NYC"})
        self.db.insert({"name": "Bob", "city": "SF"})
        self.db.insert({"name": "Charlie", "city": "NYC"})
        
        # Get distinct cities
        cities = self.db.distinct("city")
        assert len(cities) == 2
        assert "NYC" in cities
        assert "SF" in cities
    
    def test_indexing(self):
        """Test indexing functionality."""
        # Insert test data
        self.db.insert({"name": "Alice", "email": "alice@example.com"})
        self.db.insert({"name": "Bob", "email": "bob@example.com"})
        
        # Create index
        self.db.create_index("email", unique=True)
        
        # Verify index exists
        indexes = self.db.get_indexes()
        assert "email" in indexes
        
        # Test unique constraint
        with pytest.raises(ValueError):
            self.db.insert({"name": "Charlie", "email": "alice@example.com"})
    
    def test_complex_queries(self):
        """Test complex query operations."""
        # Insert test data
        self.db.insert({"name": "Alice", "age": 25, "city": "NYC", "interests": ["music"]})
        self.db.insert({"name": "Bob", "age": 30, "city": "SF", "interests": ["music"]})
        self.db.insert({"name": "Charlie", "age": 35, "city": "NYC", "interests": ["music", "sports"]})
        
        # Complex query with AND/OR
        query = {
            "$and": [
                {"age": {"$gte": 25}},
                {"$or": [
                    {"city": "NYC"},
                    {"interests": "music"}
                ]}
            ]
        }
        
        results = self.db.find(query)
        assert len(results) == 3  # All users match
    
    def test_nested_field_queries(self):
        """Test queries on nested fields."""
        self.db.insert({
            "name": "Alice",
            "profile": {
                "bio": "Software developer",
                "location": "NYC"
            }
        })
        
        # Query nested field
        results = self.db.find({"profile.bio": "Software developer"})
        assert len(results) == 1
        assert results[0].data["name"] == "Alice"
    
    def test_array_queries(self):
        """Test queries on array fields."""
        self.db.insert({
            "name": "Alice",
            "interests": ["music", "programming", "travel"]
        })
        
        # Query array contains
        results = self.db.find({"interests": "music"})
        assert len(results) == 1
        
        # Query array with $in
        results = self.db.find({"interests": {"$in": ["music", "sports"]}})
        assert len(results) == 1
    
    def test_backup_restore(self):
        """Test backup and restore functionality."""
        # Insert test data
        self.db.insert({"name": "User 1"})
        self.db.insert({"name": "User 2"})
        
        # Create backup
        backup_dir = os.path.join(self.test_dir, "backup")
        self.db.backup(backup_dir)
        
        # Clear database
        self.db.delete_all()
        assert self.db.count() == 0
        
        # Restore from backup
        self.db.restore(backup_dir)
        assert self.db.count() == 2
    
    def test_database_stats(self):
        """Test getting database statistics."""
        # Insert test data
        self.db.insert({"name": "User 1"})
        self.db.insert({"name": "User 2"})
        
        # Create index
        self.db.create_index("name")
        
        # Get stats
        stats = self.db.get_stats()
        
        assert "storage" in stats
        assert "indexes" in stats
        assert stats["total_documents"] == 2
        assert stats["indexed_fields"] == 1


class TestDocument:
    """Test cases for the Document class."""
    
    def test_document_creation(self):
        """Test creating a document."""
        data = {"name": "Test User", "age": 25}
        doc = Document(data)
        
        assert doc.data == data
        assert doc.id is not None
        assert doc.created_at is not None
        assert doc.updated_at is not None
    
    def test_document_with_custom_id(self):
        """Test creating document with custom ID."""
        data = {"name": "Test User"}
        custom_id = "custom-123"
        doc = Document(data, custom_id)
        
        assert doc.id == custom_id
    
    def test_document_update(self):
        """Test updating document data."""
        data = {"name": "Test User", "age": 25}
        doc = Document(data)
        
        original_updated_at = doc.updated_at
        
        # Update document
        doc.update({"age": 26})
        
        assert doc.data["age"] == 26
        assert doc.data["name"] == "Test User"  # Unchanged
        assert doc.updated_at > original_updated_at
    
    def test_document_to_dict(self):
        """Test converting document to dictionary."""
        data = {"name": "Test User", "age": 25}
        doc = Document(data)
        
        doc_dict = doc.to_dict()
        
        assert doc_dict["_id"] == doc.id
        assert doc_dict["data"] == data
        assert "metadata" in doc_dict
        assert "created_at" in doc_dict["metadata"]
        assert "updated_at" in doc_dict["metadata"]
    
    def test_document_from_dict(self):
        """Test creating document from dictionary."""
        original_data = {"name": "Test User", "age": 25}
        original_doc = Document(original_data)
        
        doc_dict = original_doc.to_dict()
        restored_doc = Document.from_dict(doc_dict)
        
        assert restored_doc.id == original_doc.id
        assert restored_doc.data == original_doc.data
        assert restored_doc.created_at == original_doc.created_at
        assert restored_doc.updated_at == original_doc.updated_at
    
    def test_document_equality(self):
        """Test document equality."""
        data = {"name": "Test User", "age": 25}
        doc1 = Document(data, "test-id")
        doc2 = Document(data, "test-id")
        
        assert doc1 == doc2
        
        # Different ID
        doc3 = Document(data, "different-id")
        assert doc1 != doc3
    
    def test_document_get_set(self):
        """Test document get and set methods."""
        data = {"name": "Test User", "age": 25}
        doc = Document(data)
        
        # Test get
        assert doc.get("name") == "Test User"
        assert doc.get("non-existent", "default") == "default"
        
        # Test set
        doc.set("age", 26)
        assert doc.data["age"] == 26
        assert doc.updated_at > doc.created_at


if __name__ == "__main__":
    pytest.main([__file__]) 