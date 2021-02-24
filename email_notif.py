from __future__ import print_function
from datetime import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDAR_ID = 's53k5hnu5r6r68urvm9rkk5qp0@group.calendar.google.com'

def getCreds():


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    now = datetime.now()
    print("NOW: ", now.strftime("%Y-%m-%d %H:%M:%S"))

    if not events:
        print('No upcoming events found.')
    for event in events[:1]:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start[:-6], event['summary'])

        new_start = datetime.strptime(start[:-6], '%Y-%m-%dT%H:%M:%S')
        print("NEW START: ", new_start)
        print("DIFFERNCE: ", new_start - now)

def drive():
    pass

if __name__ == '__main__':
    main()