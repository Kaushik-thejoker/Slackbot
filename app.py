import os
import sys
import json
import datetime
from fastapi import FastAPI, Response, Request
from slack_sdk import WebClient
from dotenv import load_dotenv
import requests
#from Jobs import schedule_tasks # Import the scheduling function
import uvicorn
import logging
from contextlib import asynccontextmanager

from Jobs import slack_post_message

# Load environment variables from .env file
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("START UP INIT")
    slack_post_message()
    try:
        yield
    finally:
        logging.info("Shutting down")
# Instantiating FastAPI app
app = FastAPI()


#schedule_tasks()

greetings = ["hi", "hello", "hello there", "hey"]
time_commands = ["current time", "time"]

SIGNING_SECRET = os.environ.get('SIGNING_SECRET')
slack_token = os.environ.get('SLACK_TOKEN')
VERIFICATION_TOKEN = os.environ.get('VERIFICATION_TOKEN')

# Checking if environment variables are set
if SIGNING_SECRET is None or slack_token is None or VERIFICATION_TOKEN is None:
    raise ValueError("Missing environment variables")

# Instantiating slack client
slack_client = WebClient(slack_token)

# An example of one of your FastAPI app's routes
@app.post("/slack/event")
async def event_hook(request: Request):
    json_dict = await request.json()
    if json_dict["token"] != VERIFICATION_TOKEN:
        return Response(status_code=403)

    if "type" in json_dict:
        if json_dict["type"] == "url_verification":
            response_dict = {"challenge": json_dict["challenge"]}
            return response_dict
        elif json_dict["type"] == "event_callback":
            event_data = json_dict["event"]
            if event_data.get("type") == "app_mention":
                await handle_message(event_data)
            # Add handling for other event types as needed

    return Response(status_code=500)

async def handle_message(event_data):
    async def send_reply():
        if event_data.get("subtype") is None:
            command = event_data.get("text")
            channel_id = event_data["channel"]
            if any(item in command.lower() for item in greetings):
                message_text = f"Hello <@{event_data['user']}>! :tada:"
                await slack_client.chat_postMessage(channel=channel_id, text=message_text)
            elif any(item in command.lower() for item in time_commands):
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message_text = f"The current time is {current_time}"
                await slack_client.chat_postMessage(channel=channel_id, text=message_text)

    await send_reply()
    return Response(status_code=200)

def is_valid_slack_request(request):
    # Implement request verification logic here
    return True

# FastAPI route to handle Slack command
@app.post('/nifty-momentum')
async def nifty_momentum(request: Request):
    if not is_valid_slack_request(request):
        return {"error": "Unauthorized"}, 401

    form_data = await request.form()
    number = form_data.get('text')

    if not number:
        return {"error": "Missing required parameter 'number'"}, 400

    response = requests.get(f'https://nifty-shloka-algo-cxeowxaalq-el.a.run.app/v1/nifty_momentum/{number}')

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {"error": "Failed to fetch Nifty momentum data"}, 500

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=3000, reload=True)
