from __future__ import print_function
from datetime import datetime
import time
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from notify_run import Notify
import time

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDAR_ID = 's53k5hnu5r6r68urvm9rkk5qp0@group.calendar.google.com'
DAY_SECS = 86400
notify = None
PUSH_CHANNEL = None

def authorize():
    notify = Notify()
    channel = notify.register()
    PUSH_CHANNEL = channel.endpoint
    
    print(PUSH_CHANNEL)
    time.sleep(30)
    notify.send("HEROKU SUCCESS", PUSH_CHANNEL)
    time.sleep(30)

def push(message):
    notify.send(message, PUSH_CHANNEL)

def getCreds():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def getEvents():
    creds = getCreds()


    service = build('calendar', 'v3', credentials=creds)
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    
    events = events_result.get('items', [])

    return events

print("HERE")
authorize()
push("HEROKU NOTIFICATION SYSTEM STARTING NOW")

while True:
    events = getEvents()
    
    if not events:
        time.sleep(DAY_SECS)

    else:
        for event in events:
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            new_start = datetime.strptime(start_time[:-6], '%Y-%m-%dT%H:%M:%S')

            print(event['summary'])
            print((new_start - datetime.now()).seconds - 600,  "seconds")
            time.sleep((new_start - datetime.now()).seconds - 600)
            push(event['summary'] + " in 10 minutes!")

            time.sleep(300)
            push(event['summary'] + " in 5 minutes!")

