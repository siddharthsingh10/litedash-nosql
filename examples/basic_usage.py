"""
Basic usage examples for the Personal Document Database.

This example demonstrates:
- Creating and connecting to the database
- CRUD operations (Create, Read, Update, Delete)
- Querying with different operators
- Indexing for performance
- Backup and restore functionality
"""

import os
import sys
from datetime import datetime

# Add the docstore directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from docstore.database import Database


def main():
    """Main example function."""
    print("=== Personal Document Database Examples ===\n")
    
    # Initialize database
    db = Database("example_data")
    
    # Clear any existing data
    db.delete_all()
    
    print("1. Basic CRUD Operations")
    print("-" * 30)
    
    # Create documents
    user1_id = db.insert({
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "age": 28,
        "city": "New York",
        "interests": ["programming", "music", "travel"],
        "profile": {
            "bio": "Software developer",
            "website": "https://alice.dev"
        }
    })
    
    user2_id = db.insert({
        "name": "Bob Smith",
        "email": "bob@example.com", 
        "age": 32,
        "city": "San Francisco",
        "interests": ["cooking", "photography"],
        "profile": {
            "bio": "Chef and photographer",
            "website": "https://bob.cooking"
        }
    })
    
    user3_id = db.insert({
        "name": "Charlie Brown",
        "email": "charlie@example.com",
        "age": 25,
        "city": "Chicago",
        "interests": ["sports", "reading"],
        "profile": {
            "bio": "Athlete and bookworm",
            "website": "https://charlie.sports"
        }
    })
    
    print(f"Created users: {user1_id}, {user2_id}, {user3_id}")
    
    # Read documents
    print("\n2. Reading Documents")
    print("-" * 30)
    
    # Find by ID
    alice = db.find_by_id(user1_id)
    print(f"Found Alice: {alice.data['name']} - {alice.data['email']}")
    
    # Find all documents
    all_users = db.find({})
    print(f"Total users: {len(all_users)}")
    
    # Find with query
    ny_users = db.find({"city": "New York"})
    print(f"Users in New York: {len(ny_users)}")
    
    print("\n3. Query Examples")
    print("-" * 30)
    
    # Comparison operators
    young_users = db.find({"age": {"$lt": 30}})
    print(f"Users under 30: {len(young_users)}")
    
    # Logical operators
    active_users = db.find({
        "$or": [
            {"age": {"$gte": 30}},
            {"city": "New York"}
        ]
    })
    print(f"Users 30+ or in NY: {len(active_users)}")
    
    # Nested field queries
    dev_users = db.find({"profile.bio": {"$regex": "developer"}})
    print(f"Users with 'developer' in bio: {len(dev_users)}")
    
    # Array queries
    music_lovers = db.find({"interests": "music"})
    print(f"Users interested in music: {len(music_lovers)}")
    
    print("\n4. Update Operations")
    print("-" * 30)
    
    # Update by ID
    db.update_by_id(user1_id, {"age": 29})
    updated_alice = db.find_by_id(user1_id)
    print(f"Updated Alice's age to: {updated_alice.data['age']}")
    
    # Update with query
    updated_count = db.update(
        {"city": "San Francisco"}, 
        {"profile.bio": "Updated bio"}
    )
    print(f"Updated {updated_count} users in San Francisco")
    
    # Upsert (update or insert)
    upsert_id = db.upsert(
        {"email": "david@example.com"},
        {
            "name": "David Wilson",
            "email": "david@example.com",
            "age": 35,
            "city": "Boston"
        }
    )
    print(f"Upserted David with ID: {upsert_id}")
    
    print("\n5. Indexing for Performance")
    print("-" * 30)
    
    # Create indexes
    db.create_index("email", unique=True)
    db.create_index("city")
    db.create_index("age")
    
    print(f"Created indexes on: {db.get_indexes()}")
    
    # Query using indexes (faster)
    sf_users = db.find({"city": "San Francisco"})
    print(f"Users in SF (using index): {len(sf_users)}")
    
    # Get index statistics
    index_stats = db.get_index_stats()
    print(f"Index statistics: {index_stats}")
    
    print("\n6. Advanced Queries")
    print("-" * 30)
    
    # Count documents
    total_users = db.count()
    print(f"Total users: {total_users}")
    
    # Check existence
    has_alice = db.exists({"email": "alice@example.com"})
    print(f"Alice exists: {has_alice}")
    
    # Get distinct values
    cities = db.distinct("city")
    print(f"Distinct cities: {cities}")
    
    # Complex query
    complex_query = {
        "$and": [
            {"age": {"$gte": 25}},
            {"$or": [
                {"city": "New York"},
                {"city": "San Francisco"}
            ]},
            {"interests": {"$in": ["programming", "music"]}}
        ]
    }
    
    complex_results = db.find(complex_query)
    print(f"Complex query results: {len(complex_results)} users")
    
    print("\n7. Delete Operations")
    print("-" * 30)
    
    # Delete by ID
    deleted = db.delete_by_id(user3_id)
    print(f"Deleted Charlie: {deleted}")
    
    # Delete with query
    deleted_count = db.delete({"city": "Boston"})
    print(f"Deleted {deleted_count} users from Boston")
    
    remaining_users = db.count()
    print(f"Remaining users: {remaining_users}")
    
    print("\n8. Backup and Restore")
    print("-" * 30)
    
    # Create backup
    backup_dir = "example_backup"
    db.backup(backup_dir)
    print(f"Created backup in: {backup_dir}")
    
    # Clear database
    db.delete_all()
    print("Cleared database")
    
    # Restore from backup
    db.restore(backup_dir)
    restored_count = db.count()
    print(f"Restored {restored_count} documents from backup")
    
    print("\n9. Database Statistics")
    print("-" * 30)
    
    stats = db.get_stats()
    print(f"Database stats: {stats}")
    
    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main() 