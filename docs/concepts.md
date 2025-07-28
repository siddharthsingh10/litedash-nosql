# NoSQL Database Concepts

## Understanding NoSQL vs SQL

### Traditional SQL (Relational) Databases
- **Structured Data**: Predefined schema with tables, columns, and relationships
- **ACID Properties**: Atomicity, Consistency, Isolation, Durability
- **Normalization**: Data is normalized to reduce redundancy
- **Complex Queries**: JOIN operations across multiple tables
- **Examples**: MySQL, PostgreSQL, Oracle

### NoSQL Databases
- **Flexible Schema**: No predefined structure required
- **BASE Properties**: Basically Available, Soft state, Eventual consistency
- **Denormalization**: Data can be duplicated for performance
- **Simple Queries**: Usually single-table operations
- **Examples**: MongoDB, Redis, Cassandra, Neo4j

## Document Database Deep Dive

### What is a Document?
A document is a self-contained unit of data, typically stored in JSON format. Each document contains all the information needed for a particular entity.

```json
{
  "_id": "user_123",
  "name": "John Doe",
  "email": "john@example.com",
  "profile": {
    "age": 30,
    "location": "New York",
    "interests": ["programming", "music", "travel"]
  },
  "orders": [
    {
      "order_id": "order_001",
      "items": ["laptop", "mouse"],
      "total": 1200.00
    }
  ],
  "metadata": {
    "created_at": "2024-01-01T00:00:00Z",
    "last_login": "2024-01-15T10:30:00Z"
  }
}
```

### Key Advantages of Document Databases

#### 1. Schema Flexibility
- No need to define table structure upfront
- Fields can be added/removed without migrations
- Different documents can have different fields

#### 2. Natural Data Modeling
- Documents mirror application objects
- No need for complex joins
- Hierarchical data fits naturally

#### 3. Performance Benefits
- All related data in one document
- Fewer database round trips
- Better read performance for complex data

#### 4. Developer Productivity
- JSON-like structure is familiar
- Less mapping between application and database
- Easier to evolve schemas

## Core Database Operations

### CRUD Operations

#### Create (Insert)
```python
# Insert a single document
db.insert({
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25
})

# Insert multiple documents
db.insert_many([
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 35}
])
```

#### Read (Query)
```python
# Find all documents
all_docs = db.find({})

# Find documents matching criteria
users = db.find({"age": {"$gte": 25}})

# Find by ID
user = db.find_by_id("user_123")

# Find one document
user = db.find_one({"email": "alice@example.com"})
```

#### Update
```python
# Update a single document
db.update({"email": "alice@example.com"}, {"age": 26})

# Update multiple documents
db.update_many({"age": {"$lt": 30}}, {"status": "young"})

# Upsert (update or insert)
db.upsert({"email": "alice@example.com"}, {"name": "Alice", "age": 26})
```

#### Delete
```python
# Delete documents matching criteria
db.delete({"age": {"$lt": 18}})

# Delete by ID
db.delete_by_id("user_123")

# Delete all documents
db.delete_all()
```

## Query Language Concepts

### Comparison Operators
```python
# Equal
{"age": 25}

# Greater than
{"age": {"$gt": 25}}

# Less than or equal
{"age": {"$lte": 30}}

# Not equal
{"status": {"$ne": "inactive"}}

# In array
{"category": {"$in": ["electronics", "books"]}}

# Not in array
{"category": {"$nin": ["deleted", "archived"]}}
```

### Logical Operators
```python
# AND (implicit)
{"age": {"$gte": 25}, "status": "active"}

# OR
{"$or": [{"age": {"$lt": 18}}, {"age": {"$gt": 65}}]}

# AND with OR
{
    "status": "active",
    "$or": [
        {"category": "electronics"},
        {"price": {"$gt": 100}}
    ]
}
```

### Array Operations
```python
# Array contains element
{"tags": "python"}

# Array contains all elements
{"tags": {"$all": ["python", "database"]}}

# Array size
{"tags": {"$size": 3}}

# Array element at position
{"tags.0": "python"}
```

## Indexing Concepts

### Why Indexing Matters
- **Performance**: Indexes speed up queries
- **Memory**: Indexes consume memory but improve speed
- **Trade-offs**: More indexes = faster reads, slower writes

### Types of Indexes

#### Single Field Index
```python
# Index on email field
db.create_index("email")

# Index on nested field
db.create_index("profile.age")
```

#### Compound Index
```python
# Index on multiple fields
db.create_index(["category", "price"])

# Index with sort order
db.create_index([("category", 1), ("price", -1)])
```

#### Unique Index
```python
# Ensure email uniqueness
db.create_unique_index("email")
```

### Index Strategies
1. **Identify Query Patterns**: Index fields used in WHERE clauses
2. **Consider Sort Operations**: Index fields used in ORDER BY
3. **Balance Read/Write**: More indexes = slower writes
4. **Monitor Usage**: Remove unused indexes

## Data Modeling Best Practices

### Embedding vs Referencing

#### Embedding (Denormalization)
```json
{
  "_id": "user_123",
  "name": "John Doe",
  "orders": [
    {
      "order_id": "order_001",
      "items": ["laptop", "mouse"],
      "total": 1200.00
    }
  ]
}
```

**Pros**: Faster reads, atomic updates
**Cons**: Document size limits, data duplication

#### Referencing (Normalization)
```json
// User document
{
  "_id": "user_123",
  "name": "John Doe",
  "order_ids": ["order_001", "order_002"]
}

// Order document
{
  "_id": "order_001",
  "user_id": "user_123",
  "items": ["laptop", "mouse"],
  "total": 1200.00
}
```

**Pros**: Smaller documents, no duplication
**Cons**: Multiple queries needed, eventual consistency

### When to Embed vs Reference

#### Embed When:
- Data is small and bounded
- Data is frequently accessed together
- Data doesn't change often
- One-to-few relationships

#### Reference When:
- Data is large or unbounded
- Data is accessed independently
- Data changes frequently
- Many-to-many relationships

## Consistency Models

### ACID vs BASE

#### ACID (Traditional SQL)
- **Atomicity**: All operations succeed or fail together
- **Consistency**: Database remains in valid state
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed data survives crashes

#### BASE (NoSQL)
- **Basically Available**: System responds even during failures
- **Soft State**: Data may be inconsistent temporarily
- **Eventual Consistency**: Data becomes consistent over time

### Consistency Levels

#### Strong Consistency
- All reads see the most recent write
- Slower but predictable
- Good for financial data

#### Eventual Consistency
- Reads may see stale data temporarily
- Faster and more scalable
- Good for social media, analytics

## Scalability Concepts

### Horizontal vs Vertical Scaling

#### Vertical Scaling (Scale Up)
- Add more resources to single server
- CPU, RAM, storage
- Limited by hardware constraints

#### Horizontal Scaling (Scale Out)
- Add more servers
- Distribute data across nodes
- Better for large datasets

### Sharding Strategies

#### Hash-Based Sharding
- Distribute data based on hash of key
- Even distribution
- Good for random access patterns

#### Range-Based Sharding
- Distribute data based on value ranges
- Good for range queries
- May cause uneven distribution

#### Directory-Based Sharding
- Use lookup table to find data location
- Flexible but requires coordination
- Good for complex distribution rules

## Performance Considerations

### Read Performance
- Use appropriate indexes
- Limit document size
- Use projection to return only needed fields
- Consider caching strategies

### Write Performance
- Minimize indexes on frequently updated fields
- Use bulk operations
- Consider write concerns
- Optimize document structure

### Memory Usage
- Monitor index size
- Consider data compression
- Use appropriate data types
- Clean up unused indexes

## Security Considerations

### Authentication
- User-based access control
- Role-based permissions
- API key management

### Authorization
- Document-level permissions
- Field-level access control
- Row-level security

### Data Protection
- Encryption at rest
- Encryption in transit
- Audit logging
- Data masking

## Monitoring and Maintenance

### Key Metrics
- Query performance
- Index usage
- Memory consumption
- Disk usage
- Connection count

### Maintenance Tasks
- Index optimization
- Data compaction
- Backup and recovery
- Log rotation
- Performance tuning 