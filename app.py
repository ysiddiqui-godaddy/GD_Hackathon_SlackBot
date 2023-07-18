import os
from datefinder import find_dates
from datetime import datetime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime
from dateutil.relativedelta import relativedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# Listens to incoming messages that contain "hello"
@app.message(".*")
def message_hello(message, say):
    text = message['text']
    
    # handle and change tomorrow to the date and yesterday to the date
    today = datetime.now()
    if "today" in text:
        text = text.replace("today", (today).strftime('%Y-%m-%d'))
    if "tomorrow" in text:
        text = text.replace("tomorrow", (today + relativedelta(days=1)).strftime('%Y-%m-%d'))
    elif "yesterday" in text:
        text = text.replace("yesterday", (today + relativedelta(days=-1)).strftime('%Y-%m-%d'))

    matches = find_dates(text)

    if matches:
        for match in matches:
            print("Date and time:", match)
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Do you want to schedule a meeting at {match}?"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Yes",
                        },
                        "action_id": "confirm_meeting",
                        "value": str(match)
                    }
                }
            ]
            try:
                app.client.chat_postMessage(
                    channel=message['channel'],
                    text="This is the message content.",
                    blocks=blocks,
                )
            except SlackApiError as e:
                print(f"Error posting message: {e}")


@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()


@app.action("confirm_meeting")
def handle_button_click(ack, body, say):
    # Acknowledge yes button
    ack()
    meeting_time = body['actions'][0]['value']
    say(f"Alright, scheduling your meeting at {meeting_time}...")


@app.event("app_mention")
def handle_app_mention_events(body, logger):
    logger.info(body)


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
