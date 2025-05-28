from datetime import datetime
import json
from data.kiambu_locations import get_location_info, get_suitable_crops, get_suitable_livestock
from utils.db import execute_query

# Crop database with detailed growing instructions
CROP_DATABASE = {
    'maize': {
        'growing_period': '90-120 days',
        'soil_type': 'Well-drained, fertile soil',
        'ph_range': '5.8-7.0',
        'spacing': '75-90cm between rows, 20-30cm between plants',
        'water_needs': 'Moderate, 500-800mm per growing season',
        'fertilizer': 'NPK 23:21:0 + 4S or similar',
        'pest_control': 'Regular monitoring for stem borers and armyworms',
        'harvest_time': 'When kernels are hard and dry',
        'yield': '3-5 tons per hectare under good conditions'
    },
    'beans': {
        'growing_period': '60-90 days',
        'soil_type': 'Well-drained, loamy soil',
        'ph_range': '6.0-7.0',
        'spacing': '45-60cm between rows, 10-15cm between plants',
        'water_needs': 'Moderate, 400-600mm per growing season',
        'fertilizer': 'Phosphorus-rich fertilizer',
        'pest_control': 'Watch for bean beetles and aphids',
        'harvest_time': 'When pods are dry and brittle',
        'yield': '1-2 tons per hectare'
    },
    'millet': {
        'growing_period': '60-90 days',
        'soil_type': 'Well-drained, sandy loam',
        'ph_range': '5.5-7.0',
        'spacing': '30-45cm between rows, 10-15cm between plants',
        'water_needs': 'Low, 300-500mm per growing season',
        'fertilizer': 'Nitrogen and phosphorus',
        'pest_control': 'Minimal pest issues',
        'harvest_time': 'When grains are hard',
        'yield': '1-2 tons per hectare'
    },
    'sorghum': {
        'growing_period': '90-120 days',
        'soil_type': 'Well-drained, fertile soil',
        'ph_range': '5.5-7.5',
        'spacing': '60-75cm between rows, 15-20cm between plants',
        'water_needs': 'Low to moderate, 400-600mm per growing season',
        'fertilizer': 'Nitrogen and phosphorus',
        'pest_control': 'Watch for stem borers and birds',
        'harvest_time': 'When grains are hard and dry',
        'yield': '2-4 tons per hectare'
    }
}

def init_crop_database():
    """Initialize the SQLite database for crop management"""
    conn = sqlite3.connect('crops.db')
    cursor = conn.cursor()
    
    # Create tables for crop history and user preferences
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crop_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop_name TEXT,
        location TEXT,
        weather_conditions TEXT,
        success_rate REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_preferences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop_name TEXT,
        location TEXT,
        frequency INTEGER DEFAULT 1,
        last_selected DATETIME
    )
    """)
    
    conn.commit()
    conn.close()

def get_crop_details(crop_name):
    """Get detailed growing instructions for a specific crop"""
    return CROP_DATABASE.get(crop_name.lower(), {
        'error': f'No detailed information available for {crop_name}'
    })

def record_crop_selection(crop_name, location, weather_conditions):
    """Record when a user selects a crop"""
    # Update user preferences
    update_preferences_query = """
    INSERT INTO user_preferences (crop_name, location, frequency, last_selected)
    VALUES (%s, %s, 
        COALESCE((SELECT frequency + 1 FROM user_preferences 
                  WHERE crop_name = %s AND location = %s), 1),
        CURRENT_TIMESTAMP)
    ON CONFLICT (crop_name, location) 
    DO UPDATE SET 
        frequency = user_preferences.frequency + 1,
        last_selected = CURRENT_TIMESTAMP
    """
    execute_query(update_preferences_query, (crop_name, location, crop_name, location))
    
    # Record in history
    insert_history_query = """
    INSERT INTO crop_history (crop_name, location, weather_conditions)
    VALUES (%s, %s, %s)
    """
    execute_query(insert_history_query, (crop_name, location, json.dumps(weather_conditions)))

def get_crop_recommendations(location, weather_conditions):
    """Get personalized crop recommendations based on location, history and preferences"""
    # Get location-specific recommendations
    location_info = get_location_info(location)
    if not location_info:
        return []
    
    # Get user preferences for the location
    preferences_query = """
    SELECT crop_name, frequency 
    FROM user_preferences 
    WHERE location = %s 
    ORDER BY frequency DESC, last_selected DESC
    """
    preferences = execute_query(preferences_query, (location,))
    
    # Combine location-based and preference-based recommendations
    recommendations = []
    
    # Add location-specific crops first
    for crop in location_info['suitable_crops']:
        if crop in CROP_DATABASE:
            # Find preference score if exists
            preference_score = next((freq for c, freq in preferences if c == crop), 0)
            
            recommendations.append({
                'crop': crop,
                'details': CROP_DATABASE[crop],
                'preference_score': preference_score,
                'location_specific': True,
                'climate': location_info['climate'],
                'soil': location_info['soil'],
                'altitude': location_info['altitude'],
                'rainfall': location_info['rainfall']
            })
    
    # Add other preferred crops that might be suitable
    for crop, frequency in preferences:
        if crop not in location_info['suitable_crops'] and crop in CROP_DATABASE:
            recommendations.append({
                'crop': crop,
                'details': CROP_DATABASE[crop],
                'preference_score': frequency,
                'location_specific': False
            })
    
    # Sort by location-specific first, then by preference score
    recommendations.sort(key=lambda x: (not x.get('location_specific', False), x['preference_score']), reverse=True)
    
    return recommendations

def get_livestock_recommendations(location):
    """Get livestock recommendations for a specific location"""
    location_info = get_location_info(location)
    if not location_info:
        return []
    
    return location_info['livestock']

# Initialize the database when the module is imported
init_crop_database() 