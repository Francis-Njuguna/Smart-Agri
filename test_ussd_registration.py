"""
Test script to simulate USSD registration and verify admin dashboard
"""

from utils.db import execute_query
from datetime import datetime

def simulate_farmer_registration():
    """Simulate a farmer registration through USSD"""
    try:
        # Test farmer data
        farmer_data = {
            'phone_number': '+254712345678',
            'name': 'Test Farmer',
            'location': 'limuru'
        }

        # Insert farmer into database
        query = """
        INSERT INTO farmers (phone_number, name, location, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (phone_number) 
        DO UPDATE SET 
            name = EXCLUDED.name,
            location = EXCLUDED.location,
            updated_at = EXCLUDED.updated_at
        """
        
        current_time = datetime.now()
        execute_query(query, (
            farmer_data['phone_number'],
            farmer_data['name'],
            farmer_data['location'],
            current_time,
            current_time
        ))
        
        print("Test farmer registration successful!")
        print(f"Phone: {farmer_data['phone_number']}")
        print(f"Name: {farmer_data['name']}")
        print(f"Location: {farmer_data['location']}")
        print("\nYou can now view this farmer in the admin dashboard at:")
        print("http://localhost:5001/admin/farmers")
        
    except Exception as e:
        print(f"Error registering test farmer: {str(e)}")

if __name__ == "__main__":
    print("Simulating USSD registration...")
    simulate_farmer_registration() 