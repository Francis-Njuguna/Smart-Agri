"""
Database configuration settings for PostgreSQL
"""

import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def get_db_config():
    """
    Get database configuration from environment variables
    """
    if 'DATABASE_URL' in os.environ:
        # Parse the Render PostgreSQL URL
        url = urlparse(os.environ['DATABASE_URL'])
        # Handle special characters in password
        password = url.password
        if password:
            password = password.replace('%', '%25')  # Escape % in password
        return {
            'host': url.hostname,
            'port': url.port or 5432,
            'database': url.path[1:],  # Remove leading slash
            'user': url.username,
            'password': password
        }
    else:
        # Local development configuration
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', '5432')),
            'database': os.getenv('DB_NAME', 'smart_agri'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', '')
        }

# Get database URL from environment or construct it
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    db_config = get_db_config()
    DATABASE_URL = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}" 