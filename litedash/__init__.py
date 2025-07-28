"""
LiteDash NoSQL - A lightweight document-based NoSQL database for Python.

LiteDash NoSQL is a simple, fast, and flexible document database that provides
MongoDB-like functionality in a lightweight Python package. Perfect for
prototyping, small applications, and learning NoSQL concepts.
"""

from .database import Database
from .document import Document
from .storage import Storage
from .query import QueryEngine
from .index import IndexManager, Index

__version__ = "1.0.0"
__author__ = "LiteDash NoSQL Team"

__all__ = [
    "Database",
    "Document", 
    "Storage",
    "QueryEngine",
    "IndexManager",
    "Index"
] 