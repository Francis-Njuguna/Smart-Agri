import psycopg2
from psycopg2.extras import RealDictCursor
from config import DATABASE_URL

class Farmer:
    def __init__(self, id, name, phone_number, location):
        self.id = id
        self.name = name
        self.phone_number = phone_number
        self.location = location
    
    @staticmethod
    def create(name, phone_number, location):
        """Create a new farmer record"""
        try:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        INSERT INTO farmers (name, phone_number, location)
                        VALUES (%s, %s, %s)
                        RETURNING id, name, phone_number, location
                    """, (name, phone_number, location))
                    
                    result = cur.fetchone()
                    return Farmer(
                        id=result['id'],
                        name=result['name'],
                        phone_number=result['phone_number'],
                        location=result['location']
                    )
        except Exception as e:
            raise Exception(f"Error creating farmer: {str(e)}")
    
    @staticmethod
    def get_by_phone(phone_number):
        """Get farmer by phone number"""
        try:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        SELECT id, name, phone_number, location
                        FROM farmers
                        WHERE phone_number = %s
                    """, (phone_number,))
                    
                    result = cur.fetchone()
                    if result:
                        return Farmer(
                            id=result['id'],
                            name=result['name'],
                            phone_number=result['phone_number'],
                            location=result['location']
                        )
                    return None
        except Exception as e:
            raise Exception(f"Error fetching farmer: {str(e)}")
    
    def update(self, **kwargs):
        """Update farmer information"""
        try:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Build update query dynamically
                    set_clause = ", ".join(f"{k} = %s" for k in kwargs.keys())
                    values = list(kwargs.values())
                    values.append(self.id)
                    
                    cur.execute(f"""
                        UPDATE farmers
                        SET {set_clause}
                        WHERE id = %s
                        RETURNING id, name, phone_number, location
                    """, values)
                    
                    result = cur.fetchone()
                    if result:
                        self.name = result['name']
                        self.phone_number = result['phone_number']
                        self.location = result['location']
                        return True
                    return False
        except Exception as e:
            raise Exception(f"Error updating farmer: {str(e)}")
    
    def delete(self):
        """Delete farmer record"""
        try:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM farmers WHERE id = %s", (self.id,))
                    return cur.rowcount > 0
        except Exception as e:
            raise Exception(f"Error deleting farmer: {str(e)}") 