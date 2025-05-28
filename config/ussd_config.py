# USSD Menu Configuration
USSD_MENU = {
    'main_menu': {
        'text': 'Welcome to Smart Agriculture\n1. Weather Info\n2. Market Prices\n3. Farm Tips\n4. Contact Support',
        'options': {
            '1': 'weather_menu',
            '2': 'market_menu',
            '3': 'tips_menu',
            '4': 'support_menu'
        }
    },
    'weather_menu': {
        'text': 'Weather Information\n1. Today\'s Weather\n2. Weekly Forecast\n3. Back to Main Menu',
        'options': {
            '1': 'today_weather',
            '2': 'weekly_forecast',
            '3': 'main_menu'
        }
    },
    'market_menu': {
        'text': 'Market Prices\n1. Crops\n2. Livestock\n3. Back to Main Menu',
        'options': {
            '1': 'crop_prices',
            '2': 'livestock_prices',
            '3': 'main_menu'
        }
    },
    'tips_menu': {
        'text': 'Farm Tips\n1. Crop Management\n2. Pest Control\n3. Back to Main Menu',
        'options': {
            '1': 'crop_tips',
            '2': 'pest_tips',
            '3': 'main_menu'
        }
    },
    'support_menu': {
        'text': 'Contact Support\n1. Call Support\n2. Send Message\n3. Back to Main Menu',
        'options': {
            '1': 'call_support',
            '2': 'message_support',
            '3': 'main_menu'
        }
    }
} 