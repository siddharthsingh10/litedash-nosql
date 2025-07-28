"""
Storage layer for the personal document database.
Handles persistence of documents to disk using JSON format.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from litedash.document import Document


class Storage:
    """
    Handles persistence of documents to disk.
    
    Documents are stored as JSON files in a directory structure.
    Each document is stored as a separate file for simplicity.
    """
    
    def __init__(self, data_directory: str = "data"):
        """
        Initialize storage with data directory.
        
        Args:
            data_directory: Directory to store documents
        """
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(exist_ok=True)
    
    def save_document(self, document: Document) -> None:
        """
        Save a document to disk.
        
        Args:
            document: Document to save
        """
        file_path = self.data_directory / f"{document.id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(document.to_dict(), f, indent=2, ensure_ascii=False)
    
    def load_document(self, document_id: str) -> Optional[Document]:
        """
        Load a document from disk.
        
        Args:
            document_id: ID of the document to load
            
        Returns:
            Document if found, None otherwise
        """
        file_path = self.data_directory / f"{document_id}.json"
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                doc_dict = json.load(f)
            return Document.from_dict(doc_dict)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading document {document_id}: {e}")
            return None
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document from disk.
        
        Args:
            document_id: ID of the document to delete
            
        Returns:
            True if deleted, False if not found
        """
        file_path = self.data_directory / f"{document_id}.json"
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    
    def list_document_ids(self) -> List[str]:
        """
        List all document IDs in storage.
        
        Returns:
            List of document IDs
        """
        document_ids = []
        for file_path in self.data_directory.glob("*.json"):
            document_id = file_path.stem
            document_ids.append(document_id)
        return document_ids
    
    def load_all_documents(self) -> List[Document]:
        """
        Load all documents from disk.
        
        Returns:
            List of all documents
        """
        documents = []
        for document_id in self.list_document_ids():
            document = self.load_document(document_id)
            if document:
                documents.append(document)
        return documents
    
    def clear_all(self) -> None:
        """Delete all documents from storage."""
        for file_path in self.data_directory.glob("*.json"):
            file_path.unlink()
    
    def document_exists(self, document_id: str) -> bool:
        """
        Check if a document exists in storage.
        
        Args:
            document_id: ID of the document to check
            
        Returns:
            True if document exists, False otherwise
        """
        file_path = self.data_directory / f"{document_id}.json"
        return file_path.exists()
    
    def get_storage_info(self) -> Dict[str, Any]:
        """
        Get information about storage.
        
        Returns:
            Dictionary with storage statistics
        """
        document_ids = self.list_document_ids()
        total_size = sum(
            (self.data_directory / f"{doc_id}.json").stat().st_size
            for doc_id in document_ids
        )
        
        return {
            "document_count": len(document_ids),
            "total_size_bytes": total_size,
            "data_directory": str(self.data_directory.absolute())
        }
    
    def backup_documents(self, backup_directory: str) -> None:
        """
        Create a backup of all documents.
        
        Args:
            backup_directory: Directory to store backup
        """
        backup_path = Path(backup_directory)
        backup_path.mkdir(exist_ok=True)
        
        for document_id in self.list_document_ids():
            source_file = self.data_directory / f"{document_id}.json"
            backup_file = backup_path / f"{document_id}.json"
            
            with open(source_file, 'r', encoding='utf-8') as src:
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
    
    def restore_documents(self, backup_directory: str) -> None:
        """
        Restore documents from backup.
        
        Args:
            backup_directory: Directory containing backup
        """
        backup_path = Path(backup_directory)
        if not backup_path.exists():
            raise ValueError(f"Backup directory {backup_directory} does not exist")
        
        # Clear existing documents
        self.clear_all()
        
        # Restore from backup
        for backup_file in backup_path.glob("*.json"):
            document_id = backup_file.stem
            target_file = self.data_directory / f"{document_id}.json"
            
            with open(backup_file, 'r', encoding='utf-8') as src:
                with open(target_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read()) 