"""
Database configuration settings for PostgreSQL
"""

# PostgreSQL database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'smart_agri',
    'user': 'postgres',
    'password': 'kanyau123.'  # Update this with your actual PostgreSQL password
}

# Database connection string
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}" 