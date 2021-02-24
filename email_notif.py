from __future__ import print_function
from datetime import datetime
import time
import pickle
import os.path
from push import push
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDAR_ID = 's53k5hnu5r6r68urvm9rkk5qp0@group.calendar.google.com'
DAY_SECS = 86400

def getCreds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    return creds

def getEvents():
    creds = getCreds()

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    now = datetime.now()
    print("NOW: ", now.strftime("%Y-%m-%d %H:%M:%S"))

    return events

    # for event in events[:1]:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start[:-6], event['summary'])

    #     new_start = datetime.strptime(start[:-6], '%Y-%m-%dT%H:%M:%S')
    #     print("NEW START: ", new_start)
    #     print("DIFFERENCE: ", (new_start - now).seconds)

def drive():
    while True:
        events = getEvents()
        
        if not events:
            time.sleep(DAY_SECS)

        else:
            for event in events:
                print("EVENT SEEN")
                start_time = event['start'].get('dateTime', event['start'].get('date'))
                
                new_start = datetime.strptime(start_time[:-6], '%Y-%m-%dT%H:%M:%S')
                message = event['summary']
                
                print("SLEEPING FOR ", (new_start - datetime.now()).seconds - 600, " SECONDS")

                time.sleep((new_start - datetime.now()).seconds - 300)
                push(event['summary'] + " in 10 minutes!")

print("STARTING NOW!")
drive()