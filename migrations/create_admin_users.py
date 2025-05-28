"""
Create admin_users table migration
"""

from utils.db import execute_query

def create_admin_users_table():
    """Create the admin_users table"""
    query = """
    CREATE TABLE IF NOT EXISTS admin_users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    execute_query(query)
    print("Admin users table created successfully")

if __name__ == "__main__":
    create_admin_users_table() 