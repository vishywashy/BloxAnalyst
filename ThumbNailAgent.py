import asyncio
import httpx

async def download_limited_item_png(asset_id: int, filename:str):
    # 1. Targets the verified endpoint path found on the Creator Hub portal
    url = "https://thumbnails.roblox.com/v1/assets"
    
    # 2. Configures the exact documentation query parameter mappings
    params = {
        "assetIds": str(asset_id),
        "size": "420x420",
        "format": "Png",
        "isCircular": "false"
    }
    
    # Standard desktop agent context validation
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            # First request: Pull the metadata payload
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            payload = response.json()
            data_list = payload.get("data", [])
            
            if data_list and len(data_list) > 0:
                # Target the first indexed dictionary object in the array payload
                item_data = data_list[0]
                
                if item_data.get("state") == "Completed":
                    cdn_url = item_data.get("imageUrl")
                    print(f"CDN Image Link Located: {cdn_url}")
                    
                    # Second request: Fetch raw binary bytes straight from the CDN path
                    print(f"Streaming file down to disk as '{filename}'...")
                    image_response = await client.get(cdn_url)
                    image_response.raise_for_status()
                    
                    # Write the image contents locally
                    with open(filename, "wb") as f:
                        f.write(image_response.content)
                    
                    print("Download finalized successfully!")
                    return True
                else:
                    print(f"Render engine state is not ready: {item_data.get('state')}")
            else:
                print("Server returned an empty data list block.")
                
        except httpx.HTTPStatusError as exc:
            print(f"HTTP Server Connection Error: {exc.response.status_code}")
        except Exception as exc:
            print(f"Internal script exception occurred: {exc}")
            
    return False











    
