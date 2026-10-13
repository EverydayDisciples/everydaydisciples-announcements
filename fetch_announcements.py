import os
import json
import requests

TENANT = os.environ["AZURE_TENANT_ID"]
CLIENT = os.environ["AZURE_CLIENT_ID"]
SECRET = os.environ["AZURE_CLIENT_SECRET"]

# Get access token
token = requests.post(
    f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/token",
    data={
        "grant_type": "client_credentials",
        "client_id": CLIENT,
        "client_secret": SECRET,
        "scope": "https://graph.microsoft.com/.default"
    }
).json()["access_token"]

headers = {
    "Authorization": f"Bearer {token}"
}

# Find Announcements.xlsx
url = (
    "https://graph.microsoft.com/v1.0/users/"
    "nwcoanadmin@everydaydisciples.org/drive/root/search(q='Announcements.xlsx')"
)

result = requests.get(url, headers=headers)
result.raise_for_status()

data = result.json()

print(json.dumps(data, indent=2))

with open("announcements.json", "w") as f:
    json.dump(
        [{
            "title": "Workbook Search",
            "date": "Now",
            "message": "Searching OneDrive for Announcements.xlsx"
        }],
        f,
        indent=2
    )
