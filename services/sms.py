import africastalking
from config import SMS_MENU
from models.farmer import Farmer
from services.weather import get_weather
from services.market import get_market_prices
from services.crop_manager import get_crop_recommendations, get_livestock_recommendations
from data.kiambu_locations import get_location_info

def format_crop_recommendation(recommendation):
    """Format a crop recommendation into a readable message"""
    details = recommendation['details']
    location_info = f"\nClimate: {recommendation.get('climate', 'N/A')}"
    location_info += f"\nSoil: {recommendation.get('soil', 'N/A')}"
    location_info += f"\nAltitude: {recommendation.get('altitude', 'N/A')}"
    location_info += f"\nRainfall: {recommendation.get('rainfall', 'N/A')}"
    
    return f"""
{recommendation['crop'].title()}:
Growing Period: {details['growing_period']}
Soil Type: {details['soil_type']}
pH Range: {details['ph_range']}
Spacing: {details['spacing']}
Water Needs: {details['water_needs']}
Fertilizer: {details['fertilizer']}
Pest Control: {details['pest_control']}
Harvest Time: {details['harvest_time']}
Expected Yield: {details['yield']}{location_info if recommendation.get('location_specific') else ''}
"""

def handle_sms(phone_number, text):
    """
    Handle SMS requests and manage menu-based interactions
    """
    # Initialize SMS service
    sms = africastalking.SMS
    
    try:
        # Get or create farmer
        farmer = Farmer.get_by_phone(phone_number)
        if not farmer:
            response = "Welcome to Smart Agriculture! Please register first using USSD by dialing *384*12345#"
            sms.send(response, [phone_number])
            return {"status": "success", "message": "Welcome message sent"}
        
        # Handle location change command
        if text.lower().startswith(('change location to', 'change my location to', 'update location to')):
            try:
                # Extract new location from the message
                new_location = text.lower().replace('change location to', '').replace('change my location to', '').replace('update location to', '').strip()
                
                # Check if location exists in Kiambu County
                location_info = get_location_info(new_location)
                if not location_info:
                    response = f"Sorry, {new_location} is not recognized as a location in Kiambu County. Please try again with a valid location."
                    sms.send(response, [phone_number])
                    return {"status": "error", "message": "Invalid location"}
                
                # Update farmer's location
                farmer.location = new_location
                farmer.save()
                
                # Get new recommendations for the location
                weather_info = get_weather(new_location)
                crop_recommendations = get_crop_recommendations(new_location, weather_info)
                livestock_recommendations = get_livestock_recommendations(new_location)
                
                response = f"Location updated to {new_location}!\n\n"
                response += f"Current weather: {weather_info}\n\n"
                
                if crop_recommendations:
                    response += "Recommended crops for your area:\n"
                    for i, rec in enumerate(crop_recommendations[:3], 1):
                        response += f"{i}. {rec['crop'].title()}\n"
                    response += "\nReply with a crop number (1-3) to get detailed information."
                
                if livestock_recommendations:
                    response += "\n\nRecommended livestock:\n"
                    response += ", ".join(livestock_recommendations)
                
            except Exception as e:
                response = "Sorry, couldn't update location. Please try again with format: 'change location to [place name]'"
        
        # Process menu selection
        elif text.strip() == '1':
            recommendations = get_crop_recommendations(farmer.location, get_weather(farmer.location))
            if recommendations:
                response = "Recommended crops for your area:\n"
                for i, rec in enumerate(recommendations[:3], 1):
                    response += f"{i}. {rec['crop'].title()}\n"
                response += "\nReply with a crop number (1-3) to get detailed information."
            else:
                response = "No crop recommendations available for your area."
        
        elif text.strip() == '2':
            recommendations = get_livestock_recommendations(farmer.location)
            if recommendations:
                response = f"Recommended livestock for {farmer.location}:\n"
                response += ", ".join(recommendations)
            else:
                response = "No livestock recommendations available for your area."
        
        elif text.strip() == '3':
            weather_info = get_weather(farmer.location)
            response = f"Weather in {farmer.location}: {weather_info}"
        
        elif text.strip() == '4':
            prices = get_market_prices()
            response = f"Current market prices: {prices}"
        
        elif text.strip() == '5':
            response = SMS_MENU
        
        # Handle crop detail requests
        elif text.strip() in ['1', '2', '3'] and farmer.last_command == '1':
            recommendations = get_crop_recommendations(farmer.location, get_weather(farmer.location))
            try:
                index = int(text.strip()) - 1
                if 0 <= index < len(recommendations):
                    response = format_crop_recommendation(recommendations[index])
                else:
                    response = "Invalid crop number. Please try again."
            except (ValueError, IndexError):
                response = "Invalid selection. Please try again."
        
        else:
            response = "Invalid option. " + SMS_MENU
        
        # Send response
        sms.send(response, [phone_number])
        return {"status": "success", "message": "Response sent"}
    
    except Exception as e:
        error_message = "Sorry, we encountered an error. Please try again later."
        sms.send(error_message, [phone_number])
        return {"status": "error", "message": str(e)} 