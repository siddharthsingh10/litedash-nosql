# Quick Start Guide

Get up and running with the Personal Document Database in minutes!

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd personal-db
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Basic Usage

### 1. Create and Connect to Database

```python
from src.database import Database

# Create a new database (or connect to existing)
db = Database("my_data")
```

### 2. Insert Documents

```python
# Insert a single document
user_id = db.insert({
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "age": 28,
    "city": "New York",
    "interests": ["programming", "music", "travel"]
})

print(f"Created user with ID: {user_id}")

# Insert multiple documents
documents = [
    {"name": "Bob Smith", "age": 32, "city": "San Francisco"},
    {"name": "Charlie Brown", "age": 25, "city": "Chicago"}
]

user_ids = db.insert_many(documents)
print(f"Created {len(user_ids)} users")
```

### 3. Query Documents

```python
# Find all documents
all_users = db.find({})
print(f"Total users: {len(all_users)}")

# Find by specific criteria
nyc_users = db.find({"city": "New York"})
print(f"Users in NYC: {len(nyc_users)}")

# Find users over 25
older_users = db.find({"age": {"$gte": 25}})
print(f"Users 25+: {len(older_users)}")

# Complex query
active_users = db.find({
    "$and": [
        {"age": {"$gte": 25}},
        {"$or": [
            {"city": "New York"},
            {"interests": "music"}
        ]}
    ]
})
print(f"Active users: {len(active_users)}")
```

### 4. Update Documents

```python
# Update by ID
db.update_by_id(user_id, {"age": 29})

# Update with query
updated_count = db.update(
    {"city": "San Francisco"}, 
    {"status": "active"}
)
print(f"Updated {updated_count} users")

# Upsert (update or insert)
upsert_id = db.upsert(
    {"email": "david@example.com"},
    {"name": "David Wilson", "email": "david@example.com", "age": 35}
)
```

### 5. Delete Documents

```python
# Delete by ID
db.delete_by_id(user_id)

# Delete with query
deleted_count = db.delete({"city": "Chicago"})
print(f"Deleted {deleted_count} users")
```

### 6. Create Indexes for Performance

```python
# Create indexes on frequently queried fields
db.create_index("email", unique=True)
db.create_index("city")
db.create_index("age")

# Get index statistics
stats = db.get_index_stats()
print(f"Index stats: {stats}")
```

### 7. Utility Operations

```python
# Count documents
total = db.count()
filtered = db.count({"age": {"$gte": 25}})

# Check existence
exists = db.exists({"email": "alice@example.com"})

# Get distinct values
cities = db.distinct("city")
print(f"Distinct cities: {cities}")

# Database statistics
stats = db.get_stats()
print(f"Database stats: {stats}")
```

### 8. Backup and Restore

```python
# Create backup
db.backup("my_backup")

# Restore from backup
db.restore("my_backup")
```

## Run the Example

See the database in action:

```bash
python3 examples/basic_usage.py
```

## Run Tests

Verify everything works:

```bash
python3 -m pytest tests/test_database.py -v
```

## Key Features

### ✅ What Works
- **CRUD Operations**: Create, Read, Update, Delete documents
- **Query Language**: MongoDB-like queries with operators
- **Indexing**: Fast lookups with unique constraints
- **Nested Fields**: Query nested objects with dot notation
- **Array Queries**: Search within arrays
- **Backup/Restore**: Data persistence and recovery
- **Type Safety**: Full type hints for better development

### 🔍 Query Operators
- **Comparison**: `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`
- **Logical**: `$and`, `$or`, `$not`
- **Array**: `$in`, `$nin`
- **Existence**: `$exists`
- **Pattern**: `$regex`

### 📊 Performance Features
- **In-Memory Indexes**: Fast lookups
- **Unique Constraints**: Data integrity
- **Statistics**: Monitor performance
- **File-Based Storage**: Simple persistence

## Next Steps

1. **Explore the Code**: Check out `src/` directory to understand the implementation
2. **Read Documentation**: See `docs/` for detailed concepts
3. **Try Real Data**: Use with your own datasets
4. **Learn More**: Study MongoDB, CouchDB, or other document databases

## Support

- **Documentation**: Check `docs/` folder
- **Examples**: See `examples/basic_usage.py`
- **Tests**: Run tests to verify functionality
- **Issues**: Report problems in the repository

Happy coding! 🚀 