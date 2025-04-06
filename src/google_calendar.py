import os
from datetime import datetime, timedelta
from tzlocal import get_localzone
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Define the scopes for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar_id(service, calendar_name):
    """Get the ID of a calendar with the specified name."""
    calendar_list = service.calendarList().list().execute()
    for calendar in calendar_list['items']:
        if calendar['summary'].lower() == calendar_name.lower():
            return calendar['id']
    return None


def event_exists(service, calendar_id, summary, start_time, end_time):
    """Check if an event with the specified summary exists in the calendar."""
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=(start_time - timedelta(hours=1)).isoformat() + 'Z',
        timeMax=(end_time + timedelta(hours=1)).isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    for event in events:
        if event['summary'] == summary:
            event_start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))  # Convert to UTC
            event_end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))  # Convert to UTC

            # Normalize time zones
            start_time_normalized = start_time.astimezone(event_start.tzinfo)
            end_time_normalized = end_time.astimezone(event_end.tzinfo)

            if event_start == start_time_normalized and event_end == end_time_normalized:
                return False  # Event exists and time matches
            return True  # Event exists but time differs
    return None  # Event does not exist


def get_event_id(service, calendar_id, summary, start_time, end_time):
    """Get the ID of an event with the specified summary and time range."""
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=(start_time - timedelta(hours=1)).isoformat() + 'Z',
        timeMax=(end_time + timedelta(hours=1)).isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    for event in events:
        if event['summary'] == summary:
            return event['id']  # Return the event ID if found
    return None  # Event not found


def create_event(service, calendar_id, event_details):
    """Create an event in the specified calendar."""
    try:
        event_result = service.events().insert(
            calendarId=calendar_id,
            body=event_details
        ).execute()
        print(f"Event created: {event_result.get('htmlLink')}\n")
    except Exception as e:
        print(f"Error creating event: {e}\n")


def delete_event(service, calendar_id, event_id):
    """Delete an event from the specified calendar."""
    try:
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        print(f"Event deleted successfully.")
    except Exception as e:
        print(f"Error deleting event: {e}")


def create_calendar_event(match):
    """Create a Google Calendar event for the specified match."""
    creds = None
    token = os.environ.get('GOOGLE_TOKEN')

    if token:
        creds = Credentials.from_authorized_user_info(eval(token), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(
                port=0, access_type='offline', prompt='consent'
            )
        os.environ['GOOGLE_TOKEN'] = creds.to_json()

    service = build('calendar', 'v3', credentials=creds)

    # Obtaining the ID of the calendar
    calendar_name = os.environ.get('GOOGLE_CALENDAR_NAME')
    calendar_id = get_calendar_id(service, calendar_name)

    if not calendar_id:
        print(f"The calendar '{calendar_name}' was not found.")
        return False

    # Creating the event in Google Calendar
    start_time = match['datetime']
    end_time = (
        datetime.fromisoformat(start_time)
        + timedelta(hours=2)).isoformat()
    summary = f"{match['local']} - {match['visitor']}"
    location = f"{match['competition']}"
    if match.get('channels'):
        description = "Canales:\n" + '\n'.join(
            f"  • {channel}" for channel in match['channels']
        )
    else:
        description = 'TV'

    time_changed = event_exists(
        service, calendar_id, summary,
        datetime.fromisoformat(start_time),
        datetime.fromisoformat(end_time)
    )

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': str(get_localzone()),
        },
        'end': {
            'dateTime': end_time,
            'timeZone': str(get_localzone()),
        },
    }

    if time_changed is None:
        # If the event does not exist, create it
        print(f"Event '{summary}' does not exist. Creating...")
        create_event(service, calendar_id, event)
        return True
    elif time_changed is True:
        # If the event exists but the time has changed, delete and recreate it
        print(f"Event '{summary}' already exists with different time. Recreating...")
        existing_event_id = get_event_id(
            service, calendar_id, summary,
            datetime.fromisoformat(start_time),
            datetime.fromisoformat(end_time)
        )
        if existing_event_id:
            delete_event(service, calendar_id, existing_event_id)
        create_event(service, calendar_id, event)
        return True
    elif time_changed is False:
        # If the event exists and the time has not changed, skip creation
        print(f"Event '{summary}' already exists.")
        return False
