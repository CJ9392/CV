import json
import os
import urllib.request

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": (
        "🤖 iPhone Duo Hunter is connected!\n\n"
        "Target: iPhone Duo\n"
        "Storage: 256 GB\n"
        "Color: Night Sky\n"
        "Pickup radius: 50 miles\n\n"
        "Telegram notification test successful."
    ),
}

request = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urllib.request.urlopen(request, timeout=20) as response:
    result = json.loads(response.read().decode("utf-8"))

if not result.get("ok"):
    raise RuntimeError("Telegram notification failed")

print("Telegram notification sent successfully.")
