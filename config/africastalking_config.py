import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Africa's Talking API Configuration
AFRICASTALKING_CONFIG = {
    'api_key': os.getenv('AFRICASTALKING_API_KEY', ''),
    'username': os.getenv('AFRICASTALKING_USERNAME', ''),
    'sandbox': os.getenv('AFRICASTALKING_SANDBOX', 'True').lower() == 'true'
}

# Initialize Africa's Talking
def init_africastalking():
    """
    Initialize Africa's Talking API with the configured credentials.
    Returns the initialized Africa's Talking client.
    """
    from africastalking.AfricasTalkingGateway import AfricasTalkingGateway
    
    return AfricasTalkingGateway(
        username=AFRICASTALKING_CONFIG['username'],
        apiKey=AFRICASTALKING_CONFIG['api_key'],
        sandbox=AFRICASTALKING_CONFIG['sandbox']
    ) 