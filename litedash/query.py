"""
Query engine for the personal document database.
Handles filtering and matching documents based on criteria.
"""

from typing import Any, Dict, List, Union
from .document import Document


class QueryEngine:
    """
    Handles querying and filtering documents.
    
    Supports basic comparison operators and logical operators.
    """
    
    def __init__(self):
        """Initialize the query engine."""
        pass
    
    def match_document(self, document: Document, query: Dict[str, Any]) -> bool:
        """
        Check if a document matches the query criteria.
        
        Args:
            document: Document to check
            query: Query criteria
            
        Returns:
            True if document matches, False otherwise
        """
        return self._match_dict(document.data, query)
    
    def _match_dict(self, data: Dict[str, Any], query: Dict[str, Any]) -> bool:
        """
        Recursively match a dictionary against query criteria.
        
        Args:
            data: Data to match against
            query: Query criteria
            
        Returns:
            True if data matches query, False otherwise
        """
        for key, value in query.items():
            if key.startswith('$'):
                # Handle logical operators
                if key == '$or':
                    if not isinstance(value, list):
                        return False
                    return any(self._match_dict(data, condition) for condition in value)
                elif key == '$and':
                    if not isinstance(value, list):
                        return False
                    return all(self._match_dict(data, condition) for condition in value)
                elif key == '$not':
                    return not self._match_dict(data, value)
                else:
                    # Unknown operator
                    return False
            else:
                # Handle field matching
                if not self._match_field(data, key, value):
                    return False
        
        return True
    
    def _match_field(self, data: Dict[str, Any], field_path: str, expected_value: Any) -> bool:
        """
        Match a specific field against a value.
        
        Args:
            data: Document data
            field_path: Path to the field (supports dot notation)
            expected_value: Expected value or comparison operator
            
        Returns:
            True if field matches, False otherwise
        """
        # Get the actual value from the data
        actual_value = self._get_nested_value(data, field_path)
        
        # Handle comparison operators
        if isinstance(expected_value, dict):
            for operator, operator_value in expected_value.items():
                if not self._apply_operator(actual_value, operator, operator_value):
                    return False
            return True
        else:
            # Simple equality - handle arrays
            if isinstance(actual_value, list):
                return expected_value in actual_value
            else:
                return actual_value == expected_value
    
    def _get_nested_value(self, data: Dict[str, Any], field_path: str) -> Any:
        """
        Get a value from nested dictionary using dot notation.
        
        Args:
            data: Dictionary to search in
            field_path: Path to the field (e.g., "user.profile.age")
            
        Returns:
            Value at the specified path, or None if not found
        """
        keys = field_path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        
        return current
    
    def _apply_operator(self, actual_value: Any, operator: str, expected_value: Any) -> bool:
        """
        Apply a comparison operator.
        
        Args:
            actual_value: Actual value from document
            operator: Comparison operator
            expected_value: Expected value
            
        Returns:
            True if comparison is true, False otherwise
        """
        if operator == '$eq':
            return actual_value == expected_value
        elif operator == '$ne':
            return actual_value != expected_value
        elif operator == '$gt':
            return self._compare_values(actual_value, expected_value) > 0
        elif operator == '$gte':
            return self._compare_values(actual_value, expected_value) >= 0
        elif operator == '$lt':
            return self._compare_values(actual_value, expected_value) < 0
        elif operator == '$lte':
            return self._compare_values(actual_value, expected_value) <= 0
        elif operator == '$in':
            if isinstance(actual_value, list):
                # If actual_value is a list, check if any element is in expected_value
                return any(item in expected_value for item in actual_value)
            else:
                # If actual_value is not a list, check if it's in expected_value
                return actual_value in expected_value
        elif operator == '$nin':
            if isinstance(actual_value, list):
                # If actual_value is a list, check if no element is in expected_value
                return not any(item in expected_value for item in actual_value)
            else:
                # If actual_value is not a list, check if it's not in expected_value
                return actual_value not in expected_value
        elif operator == '$exists':
            if expected_value:
                return actual_value is not None
            else:
                return actual_value is None
        elif operator == '$regex':
            if isinstance(actual_value, str):
                import re
                return bool(re.search(expected_value, actual_value))
            return False
        else:
            # Unknown operator
            return False
    
    def _compare_values(self, a: Any, b: Any) -> int:
        """
        Compare two values for ordering.
        
        Args:
            a: First value
            b: Second value
            
        Returns:
            -1 if a < b, 0 if a == b, 1 if a > b
        """
        try:
            if a < b:
                return -1
            elif a > b:
                return 1
            else:
                return 0
        except TypeError:
            # If comparison fails, treat as equal
            return 0
    
    def filter_documents(self, documents: List[Document], query: Dict[str, Any]) -> List[Document]:
        """
        Filter a list of documents based on query criteria.
        
        Args:
            documents: List of documents to filter
            query: Query criteria
            
        Returns:
            List of documents that match the criteria
        """
        return [doc for doc in documents if self.match_document(doc, query)]
    
    def sort_documents(self, documents: List[Document], sort_criteria: List[tuple]) -> List[Document]:
        """
        Sort documents based on criteria.
        
        Args:
            documents: List of documents to sort
            sort_criteria: List of (field_path, direction) tuples
                          direction: 1 for ascending, -1 for descending
            
        Returns:
            Sorted list of documents
        """
        def sort_key(doc):
            values = []
            for field_path, direction in sort_criteria:
                value = self._get_nested_value(doc.data, field_path)
                # Handle None values for sorting
                if value is None:
                    value = float('-inf') if direction > 0 else float('inf')
                values.append((value, direction))
            return values
        
        return sorted(documents, key=sort_key)
    
    def limit_documents(self, documents: List[Document], limit: int) -> List[Document]:
        """
        Limit the number of documents returned.
        
        Args:
            documents: List of documents
            limit: Maximum number of documents to return
            
        Returns:
            Limited list of documents
        """
        return documents[:limit]
    
    def skip_documents(self, documents: List[Document], skip: int) -> List[Document]:
        """
        Skip a number of documents.
        
        Args:
            documents: List of documents
            skip: Number of documents to skip
            
        Returns:
            List of documents with skipped ones removed
        """
        return documents[skip:]
    
    def project_documents(self, documents: List[Document], projection: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Project specific fields from documents.
        
        Args:
            documents: List of documents
            projection: Dictionary specifying which fields to include/exclude
            
        Returns:
            List of projected documents
        """
        projected = []
        
        for doc in documents:
            projected_doc = {}
            
            if not projection:
                # Include all fields
                projected_doc = doc.data.copy()
            else:
                for field, include in projection.items():
                    if include:
                        value = self._get_nested_value(doc.data, field)
                        if value is not None:
                            projected_doc[field] = value
            
            projected.append(projected_doc)
        
        return projected 