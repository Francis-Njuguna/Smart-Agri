"""
Configuration package initialization
"""

from .ussd_config import USSD_MENU
from .database import get_db_config, DATABASE_URL

__all__ = ['USSD_MENU', 'get_db_config', 'DATABASE_URL'] 