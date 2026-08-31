import requests

def get_limited_id(item_name: str) -> str | None:
    url = "https://www.rolimons.com/itemapi/itemdetails"
    
    # Crucial: A complete User-Agent header string mimics a real Windows Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    response = requests.get(url, headers=headers)
    
    # Prevent JSONDecodeError by checking if the request was actually allowed
    if response.status_code != 200:
        print(f"Blocked by Rolimon's Firewall. Status Code: {response.status_code}")
        # If it returns a 403, print the response text to see the HTML error page
        return None
        
    try:
        raw_json = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: Server responded with text/HTML instead of JSON data.")
        return None

    if not raw_json.get("success"):
        return None

    items = raw_json.get("items", {})
    
    # Clean list comprehension search matching item name safely
    return next((asset_id for asset_id, details in items.items() if details[0].lower() == item_name.lower()), None)

# Test execution
#print(get_limited_id("valkyrie helm"))  # Outputs: 21070012

