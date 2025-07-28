# DocStore 📦

[![PyPI version](https://badge.fury.io/py/docstore.svg)](https://badge.fury.io/py/docstore)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-29%20passed-brightgreen.svg)](https://github.com/docstore/docstore)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A lightweight, document-based NoSQL database for Python. DocStore provides MongoDB-like functionality in a simple, fast, and flexible package. Perfect for prototyping, small applications, and learning NoSQL concepts.

## ✨ Features

- **📄 Document Storage**: JSON-like document structure with flexible schema
- **🔍 Query Language**: MongoDB-inspired syntax with comparison and logical operators
- **⚡ Fast Indexing**: In-memory indexes for quick lookups
- **🛠️ CLI Interface**: Command-line tool for database operations
- **💾 Persistence**: File-based storage with backup/restore functionality
- **🎯 Type Safety**: Full type hints for better IDE support
- **🧪 Tested**: 29 comprehensive unit tests with 100% pass rate

## 🚀 Quick Start

### Installation

```bash
pip install docstore
```

### Python API

```python
from docstore import Database

# Create a database
db = Database("my_data")

# Insert a document
doc_id = db.insert({
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "age": 28,
    "city": "New York",
    "interests": ["programming", "music"]
})

# Find documents
users = db.find({"age": {"$gte": 25}})
nyc_users = db.find({"city": "New York"})

# Create an index for performance
db.create_index("email", unique=True)

# Get statistics
stats = db.get_stats()
print(f"Database has {stats['total_documents']} documents")
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

# Create an index
docstore index mydb email --unique

# Backup database
docstore backup mydb backup_dir
```

## 🔍 Query Language

DocStore supports a MongoDB-inspired query language:

### Comparison Operators
```python
# Greater than
db.find({"age": {"$gt": 25}})

# Less than or equal
db.find({"age": {"$lte": 30}})

# Not equal
db.find({"city": {"$ne": "NYC"}})
```

### Logical Operators
```python
# OR condition
db.find({"$or": [
    {"age": {"$gte": 25}},
    {"city": "NYC"}
]})

# AND condition
db.find({"$and": [
    {"age": {"$gte": 25}},
    {"city": "NYC"}
]})
```

### Array Queries
```python
# Array contains
db.find({"interests": "music"})

# Array operators
db.find({"interests": {"$in": ["music", "sports"]}})
db.find({"interests": {"$nin": ["gaming"]}})
```

### Nested Fields
```python
# Dot notation for nested objects
db.find({"address.city": "New York"})
```

## 📊 Performance Features

- **In-Memory Indexes**: Fast O(1) lookups for indexed fields
- **Unique Constraints**: Data integrity enforcement
- **Statistics**: Performance monitoring and insights
- **Automatic Index Management**: Index maintenance on document changes

## 🏗️ Architecture

```
docstore/
├── docstore/              # Main package
│   ├── database.py       # Core database engine
│   ├── document.py       # Document data structure
│   ├── storage.py        # Persistence layer
│   ├── query.py          # Query engine
│   ├── index.py          # Indexing system
│   └── cli.py            # Command-line interface
├── tests/                # Unit tests (29 tests)
├── examples/             # Usage examples
└── docs/                 # Documentation
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=docstore
```

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)**: Get up and running quickly
- **[Concepts](docs/concepts.md)**: Learn about NoSQL and document databases
- **[Implementation Summary](docs/implementation_summary.md)**: Technical details
- **[Build & Publish](build_and_publish.md)**: Publishing to PyPI

## 🎯 Use Cases

- **Prototyping**: Quick development and testing
- **Small Applications**: Personal projects and tools
- **Learning**: Understanding NoSQL concepts
- **Embedded Systems**: Lightweight data storage
- **Scripts**: Simple data persistence

## 🔧 Development

### Setup

```bash
# Clone the repository
git clone https://github.com/docstore/docstore.git
cd docstore

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/ -v
```

### Code Quality

- **Type Hints**: Full type annotations throughout
- **Black**: Consistent code formatting
- **Flake8**: Linting and style checking
- **MyPy**: Static type checking

## 📦 Package Information

- **Name**: `docstore`
- **Version**: 1.0.0
- **Python Support**: 3.8+
- **License**: MIT
- **Status**: Ready for production use

## 🌟 NoSQL Concepts Demonstrated

1. **Schema Flexibility**: No predefined structure required
2. **Document-Oriented Storage**: Self-contained documents
3. **Query Language**: MongoDB-inspired syntax
4. **Indexing Strategy**: In-memory indexes for performance
5. **BASE Properties**: Basically Available, Soft State, Eventual Consistency

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by MongoDB's document model
- Built for learning NoSQL concepts
- Designed for simplicity and performance

---

**DocStore** - Simple, Fast, Flexible Document Storage for Python 🚀 