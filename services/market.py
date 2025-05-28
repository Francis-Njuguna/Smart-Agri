from config import MARKET_API_URL

# Placeholder market data (replace with actual API integration)
MARKET_DATA = {
    'maize': {'price': 2500, 'unit': 'kg'},
    'beans': {'price': 3000, 'unit': 'kg'},
    'rice': {'price': 2800, 'unit': 'kg'},
    'cattle': {'price': 150000, 'unit': 'head'},
    'goats': {'price': 25000, 'unit': 'head'},
    'chickens': {'price': 5000, 'unit': 'bird'}
}

def get_market_prices(item=None):
    """
    Get market prices for agricultural products
    If item is specified, return price for that item only
    """
    try:
        if item:
            # Return price for specific item
            if item.lower() in MARKET_DATA:
                data = MARKET_DATA[item.lower()]
                return f"{item.title()}: {data['price']} KES per {data['unit']}"
            else:
                return f"Price information not available for {item}"
        
        # Return all prices
        response = "Current Market Prices:\n"
        for item, data in MARKET_DATA.items():
            response += f"{item.title()}: {data['price']} KES per {data['unit']}\n"
        
        return response.strip()
    
    except Exception as e:
        return f"Error fetching market prices: {str(e)}" 