import numpy as np
from sklearn.ensemble import RandomForestClassifier
from services.weather import get_weather
from config import MODEL_PARAMS

# Placeholder training data (replace with real data)
CROP_DATA = {
    'maize': {'temperature': 25, 'rainfall': 800, 'soil_type': 'loamy', 'season': 'rainy'},
    'beans': {'temperature': 20, 'rainfall': 600, 'soil_type': 'clay', 'season': 'rainy'},
    'rice': {'temperature': 30, 'rainfall': 1000, 'soil_type': 'clay', 'season': 'rainy'},
    'wheat': {'temperature': 15, 'rainfall': 400, 'soil_type': 'loamy', 'season': 'dry'}
}

ANIMAL_DATA = {
    'cattle': {'temperature': 25, 'rainfall': 800, 'land_size': 5, 'experience': 'high'},
    'goats': {'temperature': 30, 'rainfall': 400, 'land_size': 2, 'experience': 'medium'},
    'chickens': {'temperature': 25, 'rainfall': 600, 'land_size': 1, 'experience': 'low'}
}

def train_crop_model():
    """Train crop recommendation model"""
    X = []
    y = []
    
    for crop, features in CROP_DATA.items():
        X.append([
            features['temperature'],
            features['rainfall'],
            {'sandy': 0, 'clay': 1, 'loamy': 2, 'silt': 3}[features['soil_type']],
            {'dry': 0, 'rainy': 1}[features['season']]
        ])
        y.append(crop)
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    return model

def train_animal_model():
    """Train animal recommendation model"""
    X = []
    y = []
    
    for animal, features in ANIMAL_DATA.items():
        X.append([
            features['temperature'],
            features['rainfall'],
            features['land_size'],
            {'low': 0, 'medium': 1, 'high': 2}[features['experience']]
        ])
        y.append(animal)
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    return model

# Initialize models
crop_model = train_crop_model()
animal_model = train_animal_model()

def get_crop_recommendation(farmer):
    """Get crop recommendations for a farmer"""
    try:
        # Get weather data
        weather_info = get_weather(farmer.location)
        
        # Extract features
        features = [
            float(weather_info.split('\n')[0].split(': ')[1].replace('°C', '')),  # temperature
            float(weather_info.split('\n')[1].split(': ')[1].replace('%', '')),   # humidity as proxy for rainfall
            2,  # Default to loamy soil
            1   # Default to rainy season
        ]
        
        # Get prediction
        prediction = crop_model.predict([features])[0]
        probability = crop_model.predict_proba([features]).max()
        
        if probability > 0.5:
            return f"{prediction.title()} (confidence: {probability:.0%})"
        else:
            return "No suitable crops found for current conditions"
    
    except Exception as e:
        return f"Error getting crop recommendation: {str(e)}"

def get_animal_recommendation(farmer):
    """Get animal recommendations for a farmer"""
    try:
        # Get weather data
        weather_info = get_weather(farmer.location)
        
        # Extract features
        features = [
            float(weather_info.split('\n')[0].split(': ')[1].replace('°C', '')),  # temperature
            float(weather_info.split('\n')[1].split(': ')[1].replace('%', '')),   # humidity as proxy for rainfall
            2,  # Default land size
            1   # Default experience level
        ]
        
        # Get prediction
        prediction = animal_model.predict([features])[0]
        probability = animal_model.predict_proba([features]).max()
        
        if probability > 0.5:
            return f"{prediction.title()} (confidence: {probability:.0%})"
        else:
            return "No suitable animals found for current conditions"
    
    except Exception as e:
        return f"Error getting animal recommendation: {str(e)}" 