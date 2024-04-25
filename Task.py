import os
import requests
from slack_sdk.web import WebClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instantiate the Slack WebClient with your token
slack_client = WebClient(os.environ.get('SLACK_TOKEN'))

# Function to retrieve data from the API endpoint and send it to the 'signals' channel
def send_data_to_signals_channel():
    # Hardcoded parameter for the API endpoint
    number = 1
    
    # API endpoint to retrieve data
    api_url = f'https://nifty-shloka-algo-cxeowxaalq-el.a.run.app/v1/nifty_momentum/{number}'
    
    # Retrieve data from the API
    response = requests.get(api_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON data
        data = response.json()
        
        # Directly use the channel name 'signals'
        channel_name = 'signals'
        
        # Construct the message text with the retrieved data
        message_text = f"Here is the Nifty momentum data: {data}"
        
        # Post the message to the 'signals' channel
        slack_client.chat_postMessage(channel=channel_name, text=message_text)
        
        print("Data sent to the 'signals' channel successfully!")
    else:
        print("Failed to retrieve data from the API.")
