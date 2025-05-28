"""
Admin user model for authentication
"""

from flask_login import UserMixin
from utils.db import execute_query
from werkzeug.security import generate_password_hash, check_password_hash

class AdminUser(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        query = "SELECT id, username, password_hash FROM admin_users WHERE id = %s"
        result = execute_query(query, (user_id,))
        if result:
            return AdminUser(result[0][0], result[0][1], result[0][2])
        return None

    @staticmethod
    def get_by_username(username):
        query = "SELECT id, username, password_hash FROM admin_users WHERE username = %s"
        result = execute_query(query, (username,))
        if result:
            return AdminUser(result[0][0], result[0][1], result[0][2])
        return None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def create_admin_user(username, password):
    """Create a new admin user"""
    password_hash = generate_password_hash(password)
    query = """
    INSERT INTO admin_users (username, password_hash)
    VALUES (%s, %s)
    ON CONFLICT (username) DO NOTHING
    """
    execute_query(query, (username, password_hash)) 