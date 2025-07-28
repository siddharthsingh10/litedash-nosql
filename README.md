# DocStore

A lightweight, document-based NoSQL database for Python. DocStore provides MongoDB-like functionality in a simple, fast, and flexible package. Perfect for prototyping, small applications, and learning NoSQL concepts.

[![PyPI version](https://badge.fury.io/py/docstore.svg)](https://badge.fury.io/py/docstore)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is NoSQL?

NoSQL (Not Only SQL) databases are designed to handle large volumes of unstructured or semi-structured data. Unlike traditional relational databases that use tables with predefined schemas, NoSQL databases offer flexible data models.

### Key Characteristics of NoSQL Databases:

1. **Schema Flexibility**: No predefined structure required
2. **Horizontal Scalability**: Can scale across multiple servers
3. **High Performance**: Optimized for specific use cases
4. **Data Model Variety**: Document, Key-Value, Column-Family, Graph

### Types of NoSQL Databases:

#### 1. Document Databases
- Store data in document format (JSON, BSON, XML)
- Examples: MongoDB, CouchDB, Firebase Firestore
- Best for: Content management, catalogs, user profiles

#### 2. Key-Value Stores
- Simple key-value pairs
- Examples: Redis, DynamoDB, Memcached
- Best for: Caching, session storage, real-time analytics

#### 3. Column-Family Stores
- Store data in columns rather than rows
- Examples: Cassandra, HBase
- Best for: Time-series data, analytics, IoT

#### 4. Graph Databases
- Store data as nodes and relationships
- Examples: Neo4j, ArangoDB
- Best for: Social networks, recommendation engines

## This Project: Document Database

We're implementing a simple document-based NoSQL database that demonstrates core concepts:

### Features:
- **Document Storage**: Store JSON-like documents
- **CRUD Operations**: Create, Read, Update, Delete
- **Indexing**: Simple indexing for faster queries
- **Query Language**: Basic query capabilities
- **Persistence**: Data persistence to disk

### Architecture:
```
docstore/
├── docstore/
│   ├── database.py      # Core database engine
│   ├── document.py      # Document data structure
│   ├── index.py         # Indexing system
│   ├── query.py         # Query language
│   ├── storage.py       # Persistence layer
│   └── cli.py           # Command-line interface
├── tests/
│   └── test_database.py # Unit tests
├── examples/
│   └── basic_usage.py   # Usage examples
└── docs/
    └── concepts.md      # Detailed concepts
```

## Quick Start

### Installation

```bash
pip install docstore
```

### Basic Usage

```python
from docstore import Database

# Create a database
db = Database("my_data")

# Insert a document
doc_id = db.insert({
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "age": 28,
    "city": "New York"
})

# Find documents
users = db.find({"age": {"$gte": 25}})
print(f"Found {len(users)} users")

# Create an index for performance
db.create_index("email", unique=True)
```

### Command Line Interface

```bash
# Create a database
docstore create mydb

# Insert a document
docstore insert mydb '{"name": "Alice", "age": 25}'

# Find documents
docstore find mydb '{"age": {"$gte": 25}}'

# Get statistics
docstore stats mydb
```

## Development Setup

1. **Clone and Install**:
   ```bash
   git clone <repository-url>
   cd personal-db
   pip install -e .
   ```

2. **Run Examples**:
   ```bash
   python examples/basic_usage.py
   ```

3. **Run Tests**:
   ```bash
   python -m pytest tests/
   ```

## Core Concepts Explained

### Document Structure
```json
{
  "_id": "unique_identifier",
  "type": "user",
  "data": {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
  },
  "metadata": {
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

### Query Language
```python
# Find all users
db.find({"type": "user"})

# Find users with age > 25
db.find({"type": "user", "data.age": {"$gt": 25}})

# Find by ID
db.find_by_id("user_123")
```

### Indexing
- Automatic indexing on `_id` field
- Manual indexing on frequently queried fields
- B-tree structure for efficient lookups

## Learning Path

1. **Start with Basics**: Understand document structure and CRUD operations
2. **Explore Queries**: Learn the query language and filtering
3. **Understand Indexing**: See how indexes improve performance
4. **Study Persistence**: Learn how data is stored and retrieved
5. **Advanced Features**: Explore transactions, replication concepts

## Why Document Databases?

### Advantages:
- **Flexibility**: Schema can evolve without migrations
- **Performance**: No complex joins needed
- **Scalability**: Easy horizontal scaling
- **Developer Friendly**: Natural JSON-like structure

### Use Cases:
- Content Management Systems
- E-commerce Catalogs
- User Profiles and Preferences
- IoT Data Storage
- Real-time Analytics

## Next Steps

After understanding this simple implementation, explore:
- MongoDB (Production document database)
- CouchDB (Multi-master replication)
- Firebase Firestore (Serverless document database)
- Advanced concepts like sharding, replication, and consistency models 