import httpx
import pandas as pd



async def EconomyInfo(assetId):
    client = httpx.AsyncClient()
    #CoreFinancialURL = f"https://economy.roblox.com/v1/assets/{assetId}/resale-data"
    financialurl2 = f"https://economy.roblox.com/v1/assets/{assetId}/resale-data"
    #except Exception:
        #return None
    response2 = await client.get(financialurl2)
    await client.aclose()
    value_list = []
    date_list = []
    volumeValues = []
    Volumedates = []
    for i in range(len(response2.json()["priceDataPoints"])):

        values = response2.json()["priceDataPoints"][i]["value"]
        volumeValue = response2.json()['volumeDataPoints'][i]['value']
        Volumedate = response2.json()["volumeDataPoints"][i]["date"]
        volumeValues.append(volumeValue)
        Volumedates.append(Volumedate)
        dates = response2.json()["priceDataPoints"][i]["date"]
        value_list.append(values)
        date_list.append(dates)
    dataset = {"values":value_list, "dates":date_list}
    
    df = pd.DataFrame(dataset)
    return [response2.json(), volumeValues, Volumedates, df.describe()]


#import asyncio
#print(asyncio.run(EconomyInfo(1365767)))