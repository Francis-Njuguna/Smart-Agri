# Smart Agriculture System

A smart agriculture system that helps farmers manage their farms and receive important updates through SMS and USSD.

## Quick Start Guide

### 1. Setup Your Environment

1. Make sure you have Python installed on your computer
2. Open your terminal/command prompt
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

### 3. Set Up Your Environment Variables

1. Create a new file named `.env` in the project root
2. Add your Africa's Talking API credentials:
   ```
   AFRICASTALKING_API_KEY=your_api_key_here
   AFRICASTALKING_USERNAME=your_username_here
   AFRICASTALKING_SANDBOX=True
   ```

### 4. Run the Application

1. Start the application:
   ```bash
   python app.py
   ```
2. Open your web browser and go to: `http://localhost:5000`

## Features

- SMS notifications for farmers
- USSD menu for mobile access
- Weather updates
- Crop management
- Farm monitoring

## Need Help?

If you run into any issues:
1. Make sure all required packages are installed
2. Check that your `.env` file is properly configured
3. Ensure your Africa's Talking API credentials are correct

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a new branch
3. Making your changes
4. Submitting a pull request 