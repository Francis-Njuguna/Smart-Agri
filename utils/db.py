"""
Database utility functions for PostgreSQL connection handling
"""

import psycopg2
from psycopg2 import pool
from config.database import DB_CONFIG

# Create a connection pool
connection_pool = pool.SimpleConnectionPool(
    1,  # Minimum connections
    10,  # Maximum connections
    host=DB_CONFIG['host'],
    port=DB_CONFIG['port'],
    database=DB_CONFIG['database'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password']
)

def get_connection():
    """
    Get a connection from the pool
    """
    return connection_pool.getconn()

def release_connection(conn):
    """
    Release a connection back to the pool
    """
    connection_pool.putconn(conn)

def execute_query(query, params=None):
    """
    Execute a query and return results
    """
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            if cursor.description:  # If it's a SELECT query
                return cursor.fetchall()
            conn.commit()
            return None
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            release_connection(conn)

def init_database():
    """
    Initialize the database with required tables
    """
    create_tables_query = """
    -- Create crop_history table
    CREATE TABLE IF NOT EXISTS crop_history (
        id SERIAL PRIMARY KEY,
        crop_name VARCHAR(100) NOT NULL,
        location VARCHAR(100) NOT NULL,
        weather_conditions JSONB,
        success_rate FLOAT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create user_preferences table
    CREATE TABLE IF NOT EXISTS user_preferences (
        id SERIAL PRIMARY KEY,
        crop_name VARCHAR(100) NOT NULL,
        location VARCHAR(100) NOT NULL,
        frequency INTEGER DEFAULT 1,
        last_selected TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(crop_name, location)
    );

    -- Create farmers table
    CREATE TABLE IF NOT EXISTS farmers (
        id SERIAL PRIMARY KEY,
        phone_number VARCHAR(20) UNIQUE NOT NULL,
        name VARCHAR(100),
        location VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create index on frequently queried columns
    CREATE INDEX IF NOT EXISTS idx_crop_history_location ON crop_history(location);
    CREATE INDEX IF NOT EXISTS idx_user_preferences_location ON user_preferences(location);
    CREATE INDEX IF NOT EXISTS idx_farmers_phone ON farmers(phone_number);
    """
    
    try:
        execute_query(create_tables_query)
        print("Database tables initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise e 