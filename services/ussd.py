import africastalking
from config import USSD_MENU
from models.farmer import Farmer
from services.weather import get_weather
from services.market import get_market_prices
from models.recommendation import get_crop_recommendation, get_animal_recommendation

def handle_ussd(session_id, phone_number, text):
    """
    Handle USSD requests and manage menu navigation
    """
    # Split the text into a list of user inputs
    user_inputs = text.split('*')
    
    # If this is the first request (text is empty)
    if not text:
        return "CON" + USSD_MENU['main']
    
    # Get the current menu level
    menu_level = len(user_inputs)
    
    # Handle registration flow
    if user_inputs[0] == '1':
        if menu_level == 1:
            return "CON" + USSD_MENU['register']
        elif menu_level == 2:
            # Store name temporarily
            return "CON" + USSD_MENU['location']
        elif menu_level == 3:
            # Store location and complete registration
            try:
                farmer = Farmer.create(
                    phone_number=phone_number,
                    name=user_inputs[1],
                    location=user_inputs[2]
                )
                return "CON Registration successful! " + USSD_MENU['main']
            except Exception as e:
                return "END Registration failed. Please try again later."
    
    # Handle crop recommendations
    elif user_inputs[0] == '2':
        try:
            farmer = Farmer.get_by_phone(phone_number)
            if not farmer:
                return "END Please register first by selecting option 1"
            
            recommendation = get_crop_recommendation(farmer)
            return f"END Recommended crops: {recommendation}"
        except Exception as e:
            return "END Failed to get recommendations. Please try again later."
    
    # Handle animal recommendations
    elif user_inputs[0] == '3':
        try:
            farmer = Farmer.get_by_phone(phone_number)
            if not farmer:
                return "END Please register first by selecting option 1"
            
            recommendation = get_animal_recommendation(farmer)
            return f"END Recommended animals: {recommendation}"
        except Exception as e:
            return "END Failed to get recommendations. Please try again later."
    
    # Handle weather information
    elif user_inputs[0] == '4':
        try:
            farmer = Farmer.get_by_phone(phone_number)
            if not farmer:
                return "END Please register first by selecting option 1"
            
            weather_info = get_weather(farmer.location)
            return f"END Weather: {weather_info}"
        except Exception as e:
            return "END Failed to get weather information. Please try again later."
    
    # Handle market prices
    elif user_inputs[0] == '5':
        try:
            prices = get_market_prices()
            return f"END Market Prices: {prices}"
        except Exception as e:
            return "END Failed to get market prices. Please try again later."
    
    # Invalid option
    else:
        return "END Invalid option selected. Please try again." 