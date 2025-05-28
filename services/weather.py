import requests
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv
from .crop_manager import get_crop_details, record_crop_selection, get_crop_recommendations

# Load environment variables
load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')

def get_crop_recommendation(temp, humidity, rainfall):
    """Recommend crops based on weather conditions"""
    recommendations = []
    
    # Temperature-based recommendations
    if temp < 10:
        recommendations.append({
            'crop': 'winter_wheat',
            'reason': 'Cold-resistant crop suitable for low temperatures',
            'details': get_crop_details('winter_wheat')
        })
    elif temp > 35:
        recommendations.append({
            'crop': 'okra',
            'reason': 'Heat-tolerant crop suitable for high temperatures',
            'details': get_crop_details('okra')
        })
    
    # Rainfall-based recommendations
    if rainfall > 50:
        recommendations.append({
            'crop': 'rice',
            'reason': 'Water-loving crop suitable for high rainfall',
            'details': get_crop_details('rice')
        })
    elif rainfall < 10:
        recommendations.append({
            'crop': 'millet',
            'reason': 'Drought-resistant crop suitable for low rainfall',
            'details': get_crop_details('millet')
        })
    
    # Ideal conditions
    if 20 <= temp <= 30 and 30 <= humidity <= 70:
        recommendations.append({
            'crop': 'maize',
            'reason': 'Ideal conditions for maize cultivation',
            'details': get_crop_details('maize')
        })
        recommendations.append({
            'crop': 'beans',
            'reason': 'Ideal conditions for bean cultivation',
            'details': get_crop_details('beans')
        })
    
    return recommendations

def get_weather(location):
    """Get weather information for a location"""
    try:
        # First get coordinates for the location
        geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}"
        geo_response = requests.get(geocode_url)
        geo_data = geo_response.json()
        
        if not geo_data:
            return {"error": "Location not found"}
        
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        
        # Get weather forecast
        weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(weather_url)
        data = response.json()
        
        # Store in SQLite database
        conn = sqlite3.connect('weather.db')
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecast (
            location TEXT,
            date TEXT,
            temp REAL,
            humidity INTEGER,
            rainfall REAL,
            wind_speed REAL
        )
        """)
        
        # Process and store forecast data
        forecast_data = []
        for entry in data['list']:
            dt = entry['dt_txt']
            temp = entry['main']['temp']
            humidity = entry['main']['humidity']
            wind = entry['wind']['speed']
            rain = entry.get('rain', {}).get('3h', 0)
            
            weather_conditions = {
                'temperature': temp,
                'humidity': humidity,
                'rainfall': rain,
                'wind_speed': wind
            }
            
            # Get crop recommendations
            crop_recommendations = get_crop_recommendation(temp, humidity, rain)
            
            # Get personalized recommendations based on user history
            personalized_recommendations = get_crop_recommendations(location, weather_conditions)
            
            cursor.execute("""
            INSERT OR REPLACE INTO forecast 
            VALUES (?, ?, ?, ?, ?, ?)
            """, (location, dt, temp, humidity, rain, wind))
            
            forecast_data.append({
                'datetime': dt,
                'temperature': temp,
                'humidity': humidity,
                'rainfall': rain,
                'wind_speed': wind,
                'crop_recommendations': crop_recommendations,
                'personalized_recommendations': personalized_recommendations
            })
        
        conn.commit()
        conn.close()
        
        return {
            'location': location,
            'forecast': forecast_data[:5],  # Return next 5 forecasts
            'current_conditions': forecast_data[0] if forecast_data else None
        }
        
    except Exception as e:
        return {"error": str(e)}

def record_crop_choice(location, crop_name, weather_conditions):
    """Record a user's crop choice for future recommendations"""
    record_crop_selection(crop_name, location, weather_conditions) 