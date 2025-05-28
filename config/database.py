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
    if 'DATABASE_URL' in os.environ:
        # Render PostgreSQL URL
        return os.environ['DATABASE_URL']
    else:
        # Local development configuration
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'smart_agri'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', '')
        }

# PostgreSQL database configuration
DB_CONFIG = get_db_config()

# Database connection string
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}" 