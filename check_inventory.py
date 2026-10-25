import json
import os
import urllib.request
import urllib.parse
import urllib.error

# =====================================
# iPHONE DUO HUNTER CONFIGURATION
# =====================================

PRODUCT = "iPhone Duo 256GB Night Sky AT&T"
PART_NUMBER = "MK1F4LL/A"

PRODUCT_URL = (
    "https://www.apple.com/shop/buy-iphone/"
    "iphone-duo/7.6-inch-display-256gb-night-sky-att"
)

LOCATIONS = {
    "Philadelphia": "19103",
    "New Jersey": "08540",
    "New York City": "10001",
    "Long Island": "11743",
    "Delaware": "19801",
    "Baltimore": "21201",
    "Maryland": "20814",
}

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


# =====================================
# TELEGRAM NOTIFICATION
# =====================================

def send_telegram(message):

    if not TOKEN or not CHAT_ID:
        raise RuntimeError("Telegram secrets are missing")

    url = (
        f"https://api.telegram.org/"
        f"bot{TOKEN}/sendMessage"
    )

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        },
        method="POST",
    )

    with urllib.request.urlopen(
        request, timeout=20
    ) as response:
        result = json.load(response)

    if not result.get("ok"):
        raise RuntimeError("Telegram notification failed")

    print("📲 Telegram alert sent!")


# =====================================
# CHECK APPLE INVENTORY
# =====================================

print("🤖 iPhone Duo Hunter")
print(f"Searching for: {PRODUCT}")

available_stores = set()
successful_checks = 0

for city, zipcode in LOCATIONS.items():

    print(f"\n🔍 Checking {city} ({zipcode})")

    params = urllib.parse.urlencode({
        "pl": "true",
        "location": zipcode,
        "parts.0": PART_NUMBER,
    })

    url = (
        "https://www.apple.com/shop/retail/"
        "pickup-message?" + params
    )

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(
            request, timeout=20
        ) as response:
            data = json.load(response)

        stores = data.get("body", {}).get("stores")

        if not isinstance(stores, list):
            print("Unexpected inventory response")
            continue

        successful_checks += 1

        for store in stores:

            name = store.get(
                "storeName", "Unknown Store"
            )

            availability = (
                store.get("partsAvailability", {})
                .get(PART_NUMBER, {})
            )

            status = availability.get(
                "pickupDisplay", "unknown"
            )

            print(f"{name}: {status}")

            if status == "available":
                available_stores.add(name)

    except Exception as error:
        print(f"Inventory check failed: {error}")


# =====================================
# AGGRESSIVE ALERT SYSTEM
# =====================================

print("\n================================")

if available_stores:

    stores_text = "\n".join(
        f"📍 {store}"
        for store in sorted(available_stores)
    )

    message = (
        "🚨🚨 iPHONE DUO AVAILABLE! 🚨🚨\n\n"
        f"📱 {PRODUCT}\n\n"
        "AVAILABLE STORES:\n"
        f"{stores_text}\n\n"
        "🛒 COMPLETE YOUR PURCHASE:\n"
        f"{PRODUCT_URL}\n\n"
        "⚡ Check pickup availability immediately!"
    )

    print("🎉 INVENTORY FOUND!")
    send_telegram(message)

elif successful_checks:

    print("No availability found.")

else:

    print("⚠️ Inventory could not be verified.")
    raise RuntimeError("All inventory checks failed")

print("Inventory check complete.")
