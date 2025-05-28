import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/smart_agri')

# Africa's Talking configuration
AFRICASTALKING_USERNAME = os.getenv('AFRICASTALKING_USERNAME')
AFRICASTALKING_API_KEY = os.getenv('AFRICASTALKING_API_KEY')

# Weather API configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

# USSD Menu Options
USSD_MENU = {
    'main': """
1. Register as Farmer
2. Get Crop Recommendations
3. Get Animal Recommendations
4. Weather Information
5. Market Prices
    """,
    'register': """
Please enter your name:
    """,
    'location': """
Please enter your location:
    """,
    'soil_type': """
Please select your soil type:
1. Sandy
2. Clay
3. Loamy
4. Silt
    """
}

# SMS Menu Options
SMS_MENU = """
Reply with:
1 - Get crop recommendations
2 - Get animal recommendations
3 - Get weather info
4 - Get market prices
5 - Help
    """

# AI Model Parameters
MODEL_PARAMS = {
    'crop_features': ['temperature', 'rainfall', 'soil_type', 'season'],
    'animal_features': ['temperature', 'rainfall', 'land_size', 'experience']
}

# Weather API Endpoints
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Market Data API Endpoints
MARKET_API_URL = "https://api.example.com/market"  # Replace with actual market data API 