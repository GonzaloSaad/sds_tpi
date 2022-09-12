import json
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class GoogleOAuth2Server:
    authorization_url: str
    token_url: str
    revoke_url: str


@dataclass(frozen=True)
class GoogleOAuth2Client:
    client_id: str
    client_secret: str
    authorization_args: Dict[str, str]

    @property
    def auto_refresh_kwargs(self) -> Dict[str, str]:
        return dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
        )


google_oauth2_server = GoogleOAuth2Server(
    authorization_url="https://accounts.google.com/o/oauth2/v2/auth",
    token_url="https://www.googleapis.com/oauth2/v4/token",
    revoke_url="https://oauth2.googleapis.com/revoke",
)

with open("./creds/google_client_credentials.json", "r") as file:
    google_credentials = json.load(file)

google_oauth2_client = GoogleOAuth2Client(
    client_id=google_credentials["client_id"],
    client_secret=google_credentials["client_secret"],
    authorization_args={
        "prompt": "consent",
        "access_type": "offline"
    }
)

calendar_scope = [
    "openid",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar",
]
