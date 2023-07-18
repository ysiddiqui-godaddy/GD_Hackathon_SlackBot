import os
from datefinder import find_dates
from datetime import datetime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
    
            say(f'Do you want to schedule a meeting at {match}?')
            
@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
