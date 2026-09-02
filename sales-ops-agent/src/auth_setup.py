"""
Run this once, locally, to authorize the agent against your Google account.
It opens a browser window for you to log in as austin@chanty.com and grants
Gmail read/modify and Calendar read/write access. After this runs once, the
token refreshes itself and this script doesn't need to run again unless the
token gets revoked.
"""
import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
]

CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "config/google_credentials.json")
TOKEN_PATH = os.getenv("GOOGLE_TOKEN_PATH", "config/google_token.json")


def main():
    if not os.path.exists(CREDENTIALS_PATH):
        raise FileNotFoundError(
            f"Missing {CREDENTIALS_PATH}. Download OAuth client credentials "
            f"from console.cloud.google.com and save them there first."
        )

    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    creds = flow.run_local_server(port=0)

    with open(TOKEN_PATH, "w") as f:
        f.write(creds.to_json())

    print(f"Saved token to {TOKEN_PATH}. You're good to run main.py now.")


if __name__ == "__main__":
    main()
