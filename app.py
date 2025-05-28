from flask import Flask, request, jsonify
import africastalking
import os
from dotenv import load_dotenv
from services.ussd import handle_ussd
from services.sms import handle_sms
from services.weather import get_weather
from services.market import get_market_prices

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Africa's Talking
africastalking.initialize(
    os.getenv('AFRICASTALKING_USERNAME'),
    os.getenv('AFRICASTALKING_API_KEY')
)

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Smart Agriculture API is running"}), 200

@app.route('/ussd', methods=['POST'])
def ussd_callback():
    """Handle USSD requests"""
    try:
        session_id = request.form.get('sessionId')
        phone_number = request.form.get('phoneNumber')
        text = request.form.get('text', '')
        
        response = handle_ussd(session_id, phone_number, text)
        return response
    except Exception as e:
        return str(e), 500

@app.route('/sms', methods=['POST'])
def sms_callback():
    """Handle SMS requests"""
    try:
        phone_number = request.form.get('from')
        text = request.form.get('text', '')
        
        response = handle_sms(phone_number, text)
        return jsonify(response)
    except Exception as e:
        return str(e), 500

@app.route('/weather', methods=['GET'])
def weather():
    """Get weather information for a location"""
    try:
        location = request.args.get('location')
        if not location:
            return jsonify({'error': 'Location is required'}), 400
            
        weather_data = get_weather(location)
        return jsonify(weather_data)
    except Exception as e:
        return str(e), 500

@app.route('/market', methods=['GET'])
def market():
    """Get market prices for crops/animals"""
    try:
        item = request.args.get('item')
        if not item:
            return jsonify({'error': 'Item is required'}), 400
            
        prices = get_market_prices(item)
        return jsonify(prices)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port) 