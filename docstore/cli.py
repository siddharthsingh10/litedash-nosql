"""
Command-line interface for PersonalDB.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

from .database import Database


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="DocStore - A lightweight document-based NoSQL database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a new database
  docstore create mydb

  # Insert a document
  docstore insert mydb '{"name": "Alice", "age": 25}'

  # Find documents
  docstore find mydb '{"age": {"$gte": 25}}'

  # Get database stats
  docstore stats mydb

  # Create an index
  docstore index mydb email --unique

  # Backup database
  docstore backup mydb backup_dir
        """
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="DocStore 1.0.0"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new database")
    create_parser.add_argument("name", help="Database name")
    
    # Insert command
    insert_parser = subparsers.add_parser("insert", help="Insert a document")
    insert_parser.add_argument("db_name", help="Database name")
    insert_parser.add_argument("document", help="JSON document to insert")
    
    # Find command
    find_parser = subparsers.add_parser("find", help="Find documents")
    find_parser.add_argument("db_name", help="Database name")
    find_parser.add_argument("query", help="JSON query (optional)", nargs="?")
    find_parser.add_argument("--limit", type=int, help="Limit number of results")
    find_parser.add_argument("--skip", type=int, help="Skip number of results")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update documents")
    update_parser.add_argument("db_name", help="Database name")
    update_parser.add_argument("query", help="JSON query to match documents")
    update_parser.add_argument("update_data", help="JSON data to update")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete documents")
    delete_parser.add_argument("db_name", help="Database name")
    delete_parser.add_argument("query", help="JSON query to match documents")
    
    # Count command
    count_parser = subparsers.add_parser("count", help="Count documents")
    count_parser.add_argument("db_name", help="Database name")
    count_parser.add_argument("query", help="JSON query (optional)", nargs="?")
    
    # Index command
    index_parser = subparsers.add_parser("index", help="Create an index")
    index_parser.add_argument("db_name", help="Database name")
    index_parser.add_argument("field", help="Field to index")
    index_parser.add_argument("--unique", action="store_true", help="Make index unique")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Get database statistics")
    stats_parser.add_argument("db_name", help="Database name")
    
    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Backup database")
    backup_parser.add_argument("db_name", help="Database name")
    backup_parser.add_argument("backup_dir", help="Backup directory")
    
    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore database")
    restore_parser.add_argument("db_name", help="Database name")
    restore_parser.add_argument("backup_dir", help="Backup directory")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "create":
            create_database(args.name)
        elif args.command == "insert":
            insert_document(args.db_name, args.document)
        elif args.command == "find":
            find_documents(args.db_name, args.query, args.limit, args.skip)
        elif args.command == "update":
            update_documents(args.db_name, args.query, args.update_data)
        elif args.command == "delete":
            delete_documents(args.db_name, args.query)
        elif args.command == "count":
            count_documents(args.db_name, args.query)
        elif args.command == "index":
            create_index(args.db_name, args.field, args.unique)
        elif args.command == "stats":
            get_stats(args.db_name)
        elif args.command == "backup":
            backup_database(args.db_name, args.backup_dir)
        elif args.command == "restore":
            restore_database(args.db_name, args.backup_dir)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def create_database(name: str):
    """Create a new database."""
    db = Database(name)
    print(f"Created database: {name}")


def insert_document(db_name: str, document_str: str):
    """Insert a document into the database."""
    db = Database(db_name)
    document = json.loads(document_str)
    doc_id = db.insert(document)
    print(f"Inserted document with ID: {doc_id}")


def find_documents(db_name: str, query_str: str = None, limit: int = None, skip: int = None):
    """Find documents in the database."""
    db = Database(db_name)
    
    query = {}
    if query_str:
        query = json.loads(query_str)
    
    documents = db.find(query, limit=limit, skip=skip)
    
    print(f"Found {len(documents)} documents:")
    for doc in documents:
        print(f"  ID: {doc.id}")
        print(f"  Data: {json.dumps(doc.data, indent=2)}")
        print()


def update_documents(db_name: str, query_str: str, update_data_str: str):
    """Update documents in the database."""
    db = Database(db_name)
    
    query = json.loads(query_str)
    update_data = json.loads(update_data_str)
    
    updated_count = db.update(query, update_data)
    print(f"Updated {updated_count} documents")


def delete_documents(db_name: str, query_str: str):
    """Delete documents from the database."""
    db = Database(db_name)
    
    query = json.loads(query_str)
    deleted_count = db.delete(query)
    print(f"Deleted {deleted_count} documents")


def count_documents(db_name: str, query_str: str = None):
    """Count documents in the database."""
    db = Database(db_name)
    
    query = {}
    if query_str:
        query = json.loads(query_str)
    
    count = db.count(query)
    print(f"Count: {count}")


def create_index(db_name: str, field: str, unique: bool = False):
    """Create an index on a field."""
    db = Database(db_name)
    
    db.create_index(field, unique=unique)
    print(f"Created {'unique ' if unique else ''}index on field: {field}")


def get_stats(db_name: str):
    """Get database statistics."""
    db = Database(db_name)
    
    stats = db.get_stats()
    print("Database Statistics:")
    print(json.dumps(stats, indent=2))


def backup_database(db_name: str, backup_dir: str):
    """Backup the database."""
    db = Database(db_name)
    
    db.backup(backup_dir)
    print(f"Backed up database to: {backup_dir}")


def restore_database(db_name: str, backup_dir: str):
    """Restore the database from backup."""
    db = Database(db_name)
    
    db.restore(backup_dir)
    print(f"Restored database from: {backup_dir}")


if __name__ == "__main__":
    main() 