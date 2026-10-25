import json
import urllib.request
import urllib.error

PRODUCT_URL = (
    "https://www.apple.com/shop/buy-iphone/"
    "iphone-duo/7.6-inch-display-256gb-night-sky-att"
)

ZIP_CODE = "19103"
RADIUS_MILES = 50

print("🤖 iPhone Duo Hunter")
print("Checking Apple product page...")
print(f"ZIP code: {ZIP_CODE}")
print(f"Search radius: {RADIUS_MILES} miles")

request = urllib.request.Request(
    PRODUCT_URL,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html",
    },
)

try:
    with urllib.request.urlopen(request, timeout=20) as response:
        print(f"HTTP status: {response.status}")
        print(f"Final URL: {response.url}")
        print("Product page request completed.")

except urllib.error.HTTPError as error:
    print(f"Apple returned HTTP {error.code}")

except urllib.error.URLError as error:
    print(f"Connection failed: {error.reason}")
print("\n🔍 Checking for inventory information...")

try:
    with urllib.request.urlopen(request, timeout=20) as response:
        html = response.read().decode("utf-8", errors="replace")

    print(f"Page size: {len(html)} characters")

    keywords = [
        "pickup",
        "availability",
        "storePickup",
        "pickupMessage",
        "partNumber",
    ]

    for keyword in keywords:
        count = html.lower().count(keyword.lower())
        print(f"{keyword}: {count} occurrences")

    if "storePickup" in html:
        print("Potential pickup data reference found.")
    else:
        print("No storePickup reference found.")

    print("Inventory diagnostic completed.")

except Exception as error:
    print(f"Inventory diagnostic failed: {type(error).__name__}")
