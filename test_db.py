"""
Test script to verify database connection and functionality
"""

from utils.db import execute_query, init_database
from config.database import DB_CONFIG
import json

def test_connection():
    """Test database connection"""
    try:
        # Try to execute a simple query
        result = execute_query("SELECT version();")
        print("Database connection successful!")
        print(f"PostgreSQL version: {result[0][0]}")
        return True
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return False

def test_table_creation():
    """Test table creation and basic operations"""
    try:
        # Initialize database tables
        init_database()
        print("\nTables created successfully!")

        # Test inserting a farmer
        insert_farmer = """
        INSERT INTO farmers (phone_number, name, location)
        VALUES (%s, %s, %s)
        """
        execute_query(insert_farmer, ('+254712345678', 'Test Farmer', 'limuru'))
        print("Test farmer inserted successfully!")

        # Test inserting crop preference
        insert_preference = """
        INSERT INTO user_preferences (crop_name, location, frequency)
        VALUES (%s, %s, %s)
        """
        execute_query(insert_preference, ('maize', 'limuru', 1))
        print("Test crop preference inserted successfully!")

        # Test inserting crop history
        insert_history = """
        INSERT INTO crop_history (crop_name, location, weather_conditions)
        VALUES (%s, %s, %s)
        """
        weather_data = {'temperature': 25, 'humidity': 60, 'rainfall': 0}
        execute_query(insert_history, ('maize', 'limuru', json.dumps(weather_data)))
        print("Test crop history inserted successfully!")

        # Verify data
        print("\nVerifying inserted data:")
        
        # Check farmers
        farmers = execute_query("SELECT * FROM farmers;")
        print("\nFarmers:")
        for farmer in farmers:
            print(f"Phone: {farmer[1]}, Name: {farmer[2]}, Location: {farmer[3]}")

        # Check preferences
        preferences = execute_query("SELECT * FROM user_preferences;")
        print("\nUser Preferences:")
        for pref in preferences:
            print(f"Crop: {pref[1]}, Location: {pref[2]}, Frequency: {pref[3]}")

        # Check history
        history = execute_query("SELECT * FROM crop_history;")
        print("\nCrop History:")
        for hist in history:
            print(f"Crop: {hist[1]}, Location: {hist[2]}, Weather: {hist[3]}")

        return True
    except Exception as e:
        print(f"Error testing tables: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing database connection and functionality...")
    print(f"Database: {DB_CONFIG['database']}")
    print(f"Host: {DB_CONFIG['host']}")
    print(f"Port: {DB_CONFIG['port']}")
    print(f"User: {DB_CONFIG['user']}")
    print("-" * 50)

    if test_connection():
        print("\nTesting table creation and operations...")
        test_table_creation() 