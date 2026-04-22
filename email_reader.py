from typing import Any, List, Dict
import base64
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Gmail read-only permission
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class EmailReader:
    def __init__(self):
        self.service = self.authenticate()

    def authenticate(self):
        creds = None

        # Load existing token
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        # If no valid credentials → login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save token for next time
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        # Build Gmail service
        return build("gmail", "v1", credentials=creds)

    def fetch_emails(self) -> List[Dict[str, Any]]:
        results = self.service.users().messages().list(
            userId="me", maxResults=5
        ).execute()

        messages = results.get("messages", [])
        emails = []

        for msg in messages:
            msg_data = self.service.users().messages().get(
                userId="me", id=msg["id"]
            ).execute()

            payload = msg_data.get("payload", {})
            headers = payload.get("headers", [])

            subject = ""
            sender = ""

            # Extract subject & sender
            for header in headers:
                if header["name"] == "Subject":
                    subject = header["value"]
                if header["name"] == "From":
                    sender = header["value"]

            body = ""

            # Handle email body
            parts = payload.get("parts")

            if parts:
                for part in parts:
                    if part["mimeType"] == "text/plain":
                        data = part["body"].get("data")
                        if data:
                            body = base64.urlsafe_b64decode(data).decode("utf-8")
            else:
                data = payload.get("body", {}).get("data")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8")

            emails.append(
                {
                    "subject": subject,
                    "body": body,
                    "sender": sender,
                }
            )

        return emails


# ✅ TEST BLOCK (IMPORTANT)
if __name__ == "__main__":
    print("🔐 Connecting to Gmail...")

    reader = EmailReader()
    emails = reader.fetch_emails()

    print(f"\n📩 Fetched {len(emails)} emails\n")

    for email in emails:
        print("----- EMAIL -----")
        print("From:", email["sender"])
        print("Subject:", email["subject"])
        print("Body:", email["body"][:200])
        print()