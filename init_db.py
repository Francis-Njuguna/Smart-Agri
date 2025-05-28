"""
Database initialization script
"""

from utils.db import init_database

if __name__ == "__main__":
    print("Initializing database...")
    init_database()
    print("Database initialization complete!") 