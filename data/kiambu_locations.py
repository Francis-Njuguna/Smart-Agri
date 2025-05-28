"""
Kiambu County agricultural zones and recommendations database.
This module contains detailed information about different locations in Kiambu County,
including their climate, soil conditions, and suitable agricultural activities.
"""

KIAMBU_LOCATIONS = {
    'limuru': {
        'climate': 'Upper highland humid zone',
        'soil': 'Fertile volcanic soils',
        'suitable_crops': ['tea', 'cabbage', 'irish_potato', 'maize'],
        'livestock': ['dairy_cattle'],
        'notes': 'Major tea production hub with processing facilities',
        'altitude': '2000-2300m',
        'rainfall': '1200-2000mm annually'
    },
    'lari': {
        'climate': 'High rainfall zone',
        'soil': 'Fertile soils',
        'suitable_crops': ['tea', 'cabbage', 'kale', 'spinach', 'coriander', 'pear'],
        'livestock': ['dairy_cattle'],
        'notes': 'Major pear production area',
        'altitude': '1800-2200m',
        'rainfall': '1000-1800mm annually'
    },
    'githunguri': {
        'climate': 'Upper midland zone',
        'soil': 'Fertile soils',
        'suitable_crops': ['tea', 'coffee', 'horticultural_crops'],
        'livestock': ['dairy_cattle', 'poultry', 'pigs'],
        'notes': 'Home to major dairy processing facilities',
        'altitude': '1600-2000m',
        'rainfall': '900-1600mm annually'
    },
    'gatundu': {
        'climate': 'Upper midland sub-humid zone',
        'soil': 'Well-drained soils',
        'suitable_crops': ['maize', 'beans', 'irish_potato', 'pineapple', 'coffee'],
        'livestock': ['dairy_cattle', 'poultry'],
        'notes': 'Major pineapple production area',
        'altitude': '1500-1900m',
        'rainfall': '800-1500mm annually'
    },
    'karuri': {
        'climate': 'Moderate climate',
        'soil': 'Well-drained soils',
        'suitable_crops': ['coffee', 'maize', 'horticultural_crops', 'fruits'],
        'livestock': ['dairy_cattle'],
        'notes': 'Coffee-growing zone',
        'altitude': '1400-1800m',
        'rainfall': '700-1400mm annually'
    },
    'kikuyu': {
        'climate': 'Lower highland semi-humid zone',
        'soil': 'Rich soil texture',
        'suitable_crops': ['maize', 'beans', 'banana', 'vegetables'],
        'livestock': ['dairy_cattle', 'poultry'],
        'notes': 'Supports both livestock and crop farming',
        'altitude': '1300-1700m',
        'rainfall': '600-1300mm annually'
    },
    'ruiru': {
        'climate': 'Upper midland transitional zone',
        'soil': 'Shallow, poorly drained soils',
        'suitable_crops': ['drought_resistant_crops'],
        'livestock': ['beef_cattle', 'goats'],
        'notes': 'Suitable for ranching',
        'altitude': '1200-1600m',
        'rainfall': '500-1200mm annually'
    },
    'juja': {
        'climate': 'Upper midland transitional zone',
        'soil': 'Shallow soils',
        'suitable_crops': ['drought_resistant_crops'],
        'livestock': ['beef_cattle', 'goats'],
        'notes': 'Suitable for ranching',
        'altitude': '1100-1500m',
        'rainfall': '400-1100mm annually'
    },
    'thika': {
        'climate': 'Upper midland zone',
        'soil': 'Varied soil types',
        'suitable_crops': ['pineapple', 'coffee', 'horticultural_crops'],
        'livestock': ['dairy_cattle', 'poultry'],
        'notes': 'Major agricultural processing hub',
        'altitude': '1000-1400m',
        'rainfall': '300-1000mm annually'
    }
}

def get_location_info(location_name):
    """
    Get detailed information about a specific location in Kiambu County.
    
    Args:
        location_name (str): Name of the location (case-insensitive)
        
    Returns:
        dict: Location information including climate, soil, and suitable crops
    """
    return KIAMBU_LOCATIONS.get(location_name.lower(), None)

def get_suitable_crops(location_name):
    """
    Get list of suitable crops for a specific location.
    
    Args:
        location_name (str): Name of the location (case-insensitive)
        
    Returns:
        list: List of suitable crops for the location
    """
    location_info = get_location_info(location_name)
    return location_info['suitable_crops'] if location_info else []

def get_suitable_livestock(location_name):
    """
    Get list of suitable livestock for a specific location.
    
    Args:
        location_name (str): Name of the location (case-insensitive)
        
    Returns:
        list: List of suitable livestock for the location
    """
    location_info = get_location_info(location_name)
    return location_info['livestock'] if location_info else [] 