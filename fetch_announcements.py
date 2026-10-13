import os
import json
import requests
from openpyxl import load_workbook

TENANT = os.environ["AZURE_TENANT_ID"]
CLIENT = os.environ["AZURE_CLIENT_ID"]
SECRET = os.environ["AZURE_CLIENT_SECRET"]

DRIVE_ID = "b!dxg-wVYphk2QLxIePQ89DlOz6zZ_l9dGh_YcG1-Yi0KmFLGGJtrCTq4wnl9R691p"
FILE_ID = "014RM5RVULGNO3VQ2X7ZF22XHUGXK35GRA"

# Get Graph access token
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

# Download workbook
url = (
    f"https://graph.microsoft.com/v1.0/drives/{DRIVE_ID}"
    f"/items/{FILE_ID}/content"
)

response = requests.get(url, headers=headers)
response.raise_for_status()

with open("Announcements.xlsx", "wb") as f:
    f.write(response.content)

# Read workbook
wb = load_workbook("Announcements.xlsx")
ws = wb["Announcements"]

rows = list(ws.values)

headers_row = rows[0]
data_rows = rows[1:]

announcements = []

for row in data_rows:

    item = dict(zip(headers_row, row))

    title = item.get("Title")

    # Skip blank rows
    if (
        title is None
        or str(title).strip() == ""
        or str(title).lower() == "none"
    ):
        continue

    date_value = item.get("PostedDate", "")

    try:
        if hasattr(date_value, "strftime"):
            formatted_date = date_value.strftime(
                "%B %d, %Y %I:%M %p"
            )
        else:
            formatted_date = str(date_value)
    except Exception:
        formatted_date = str(date_value)

    announcements.append({
        "title": str(item.get("Title", "")),
        "message": str(item.get("Message", "")),
        "date": formatted_date,
        "author": str(item.get("Author", ""))
    })

# Save website JSON
with open(
    "announcements.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        announcements,
        f,
        indent=2,
        ensure_ascii=False
    )

print(f"Wrote {len(announcements)} announcements")
