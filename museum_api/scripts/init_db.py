#!/usr/bin/env python3
"""
Database initialization script for Museum Bot Backend
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db.database import create_tables, engine
from config import settings


def init_database():
    """Initialize the database with all tables"""
    print(f"Connecting to database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    
    try:
        # Test connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
            print("✓ Database connection successful")
        
        # Create tables
        create_tables()
        print("✓ Database tables created successfully")
        
        print("\nDatabase initialization completed!")
        
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    init_database() 