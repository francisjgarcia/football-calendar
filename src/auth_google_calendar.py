import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Definir el alcance (Google Calendar)
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    creds = None
    # If a token file exists, try to load it
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file(
            'token.json', SCOPES)

    # If there are no valid credentials, perform the authentication process
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # If the credentials have expired, refresh them
            creds.refresh(Request())
        else:
            # If there are no credentials, perform the authentication process
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # Run the authentication process
            creds = flow.run_local_server(
                port=0, access_type='offline', prompt='consent')

        # Save the credentials in a token file
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    print("Authentication successful!")


if __name__ == '__main__':
    main()
