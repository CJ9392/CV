import json
import urllib.request
import urllib.parse
import urllib.error

# iPhone Duo Hunter
PRODUCT = "iPhone Duo 256GB Night Sky AT&T"
PART_NUMBER = "MK1F4LL/A"

# Search locations
LOCATIONS = {
    "Philadelphia": "19103",
    "New Jersey": "08540",
    "New York City": "10001",
    "Long Island": "11743",
    "Delaware": "19801",
    "Baltimore": "21201",
    "Maryland": "20814",
}

print("🤖 iPhone Duo Hunter")
print(f"Looking for: {PRODUCT}")
print("=" * 40)

available_stores = []
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
            print("⚠️ Unexpected inventory response")
            continue

        successful_checks += 1

        for store in stores:
            name = store.get("storeName", "Unknown")

            availability = (
                store.get("partsAvailability", {})
                .get(PART_NUMBER, {})
            )

            status = availability.get(
                "pickupDisplay", "unknown"
            )

            print(f"{name}: {status}")

            if status == "available":
                available_stores.append(name)

    except Exception as error:
        print(f"⚠️ Check failed: {error}")

print("\n" + "=" * 40)

if available_stores:
    print("🎉 AVAILABLE AT:")
    for store in sorted(set(available_stores)):
        print(store)

elif successful_checks:
    print("No availability found in checked stores.")

else:
    print("⚠️ Inventory could not be verified.")

print("\nInventory check complete.")
