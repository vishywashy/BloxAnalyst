import httpx
import pandas as pd
from Plotter import PlotGraph
from ollama import AsyncClient





    
    
    
    







async def EconomyInfo(collectibleItemId):
    client = httpx.AsyncClient()
    print(collectibleItemId)
    CoreFinancialURL = f"https://apis.roblox.com/marketplace-sales/v1/item/{collectibleItemId}/resale-data"
    #except Exception:
        #return None
    response2 = await client.get(CoreFinancialURL)
    value_list = []
    date_list = []
    for i in range(len(response2.json()["priceDataPoints"])-1):

        values = response2.json()["priceDataPoints"][i]["value"]
        dates = response2.json()["priceDataPoints"][i]["date"]
        value_list.append(values)
        date_list.append(dates)
    dataset = {"values":value_list, "dates":date_list}
    df = pd.DataFrame(dataset)
    system_rules = (
           """You are an expert Data Scientist specializing in quantitative statistical analysis. 
    Your task is to provide a lean, high-density analytical breakdown of a pandas .describe() matrix.
    
    CRITICAL INFERENCE CONSTRAINTS:
    1.STRICT TRUTH:DON'T ASSUME ONLY USE THE DATASET AND EXPLAIN IT
    2.NO HALLUCINATION:ENSURE WHAT YOU ARE SAYING IS TRUE AND ENSURE IT IS CORRECT. ENSURE NO MISTAKES IN WHAT YOU ARE DOING
    3.ANALYSE THE DATA EFFICIENTLY AND PRODUCE A HIGH QUALITY SUMMARY FROM THE DATA. ENSURE ANY STATEMENTS SAID SHOULD BE TRUE.
    
    """
        )
    response = await AsyncClient().generate(
         model="gemma3:4b",
        prompt=f"""
        INSTRUCTIONS:{system_rules}
    
        Apply the instructions you were given to:
        {df.describe().to_markdown()}. Ensure your summary is between 100-150 words.""",
        
        options={
            "temperature": 0.0,  # Keeps the RAM cache small and fast
            "num_thread": 8  # Prevents hyper-thread traffic jams on your Ryzen 7
        } # Absolute zero completely turns off creative guessing
    )
    return [response2.json(), response["response"]]


#import asyncio
#asyncio.run(EconomyInfo(1365767))
    
    



        

