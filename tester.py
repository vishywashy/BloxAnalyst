import httpx
from ReactTools import *
from EconomyAgent import EconomyInfo
import asyncio
from ConsolidatorAgent import Analyser
from RolimonAgent import rolimonExtractor
from ThumbNailAgent import download_limited_item_png
from Plotter import PlotRAPGraph, PlotVolumeGraph
import requests
import rolimons
from AssetIDreturner import get_limited_id
async def catalogAgent(search_term: str):
    """Returns the asset id for a specific item"""
    url = "https://catalog.roblox.com/v1/search/items/details"
    search_term = search_term
    # Keyword matches the search; Limit=10 is the lowest Roblox accepts,
    # but we will manually slice out the first result inside the code.
    params = {
        "id":get_limited_id(search_term) # True = Crucial for Limiteds that are no longer actively on-sale by Roblox
    }
    client = httpx.AsyncClient()
    response = await client.get(url, params=params)
    await client.aclose()
    print(response.status_code)
    
    # Check for HTTP status errors (like 429 rate limits or 400 bad requests)
    if response.status_code == 200:
                rolimon, economy = await asyncio.gather(rolimonExtractor(get_limited_id(search_term)), EconomyInfo(response.json()["data"][0]["collectibleItemId"]))
                
                PlotRAPGraph(economy[0], rolimon[2], rolimon[0], rolimon[1], search_term)
                print("Done")
                PlotVolumeGraph(economy[1], economy[2], search_term)
                response = await download_limited_item_png(get_limited_id(search_term), search_term+".png")
                
                print("Plotted")
                if response:
                    print(Analyser(rolimon[-1], economy[-1], search_term))
                return [rolimon, economy]







import asyncio
asyncio.run(catalogAgent("Shaggy"))
