"""
Database configuration settings for PostgreSQL
"""

import os
from dotenv import load_dotenv

load_dotenv()

def get_db_config():
    """
    Get database configuration from environment variables
    """
    # Get DATABASE_URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return database_url

# Get database URL
DATABASE_URL = get_db_config() 