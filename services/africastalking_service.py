from config.africastalking_config import init_africastalking

class AfricasTalkingService:
    def __init__(self):
        self.gateway = init_africastalking()

    def send_sms(self, phone_number, message):
        """
        Send an SMS message using Africa's Talking API
        
        Args:
            phone_number (str): The recipient's phone number
            message (str): The message to send
            
        Returns:
            dict: Response from Africa's Talking API
        """
        try:
            response = self.gateway.sendMessage(phone_number, message)
            return response
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
            return None

    def send_ussd_push(self, phone_number, menu_text):
        """
        Send a USSD push notification
        
        Args:
            phone_number (str): The recipient's phone number
            menu_text (str): The USSD menu text to display
            
        Returns:
            dict: Response from Africa's Talking API
        """
        try:
            response = self.gateway.sendUssdPush(phone_number, menu_text)
            return response
        except Exception as e:
            print(f"Error sending USSD push: {str(e)}")
            return None

    def get_balance(self):
        """
        Get the current account balance
        
        Returns:
            dict: Response containing balance information
        """
        try:
            response = self.gateway.getBalance()
            return response
        except Exception as e:
            print(f"Error getting balance: {str(e)}")
            return None 