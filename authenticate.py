#Initialize the OAuth flow requesting both Gmail and Tasks scopes. This script generates a local login prompt and builds the service objects you need to interact with the APIs.
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/tasks']

# For local development, this opens your browser to log in
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

# Save credentials for future use (avoids logging in every time)
with open('token.pickle', 'wb') as token:
    pickle.dump(creds, token)

gmail = build('gmail', 'v1', credentials=creds)
tasks = build('tasks', 'v1', credentials=creds)