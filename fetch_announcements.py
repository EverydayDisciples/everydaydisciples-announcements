import os
import json
import requests

TENANT = os.environ["AZURE_TENANT_ID"]
CLIENT = os.environ["AZURE_CLIENT_ID"]
SECRET = os.environ["AZURE_CLIENT_SECRET"]

token_url = f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/token"

response = requests.post(
    token_url,
    data={
        "grant_type": "client_credentials",
        "client_id": CLIENT,
        "client_secret": SECRET,
        "scope": "https://graph.microsoft.com/.default"
    }
)

response.raise_for_status()

token = response.json()["access_token"]

headers = {
    "Authorization": f"Bearer {token}"
}

test = requests.get(
    "https://graph.microsoft.com/v1.0/sites?search=nwcoan",
    headers=headers
)

result = test.json()

with open("announcements.json", "w") as f:
    json.dump(
        [{
            "title": "Graph Authentication Successful",
            "date": "Today",
            "message": "GitHub Actions connected to Microsoft Graph."
        }],
        f,
        indent=2
    )

print(json.dumps(result, indent=2))
