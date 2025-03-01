import os
import pickle
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define OAuth scopes required for Gmail API
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# paths for token storage and OAuth credentials
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
CREDENTIALS_FILE = os.path.join(BASE_DIR, "my_oauth.json")  # OAuth credentials JSON file
TOKEN_FILE = os.path.join(BASE_DIR, "token.pickle")  # Token storage file


def authenticate_gmail():
    """Authenticate user with OAuth and generate token.pickle file for future use."""
    creds = None

    # Load token agr hai to
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    # agr token nhi to new token
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)

        # save token for future use
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    return creds

# send email using OAuth
def send_email_oauth(to_email, subject, message_body):

    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)

    # Create an email message
    email_msg = MIMEText(message_body)
    email_msg["to"] = to_email
    email_msg["subject"] = subject
    raw = base64.urlsafe_b64encode(email_msg.as_bytes()).decode()

    message = {"raw": raw}
    send_message = service.users().messages().send(userId="me", body=message).execute()
    print(f"Email sent successfully! Message ID: {send_message['id']}")


# manually chalana for testing
if __name__ == "__main__":
    print("Run this script manually to authenticate with Gmail API and store the token.")
