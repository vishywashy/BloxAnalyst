import rolimons
from datetime import datetime
from datetime import timezone
import pandas as pd
from ollama import AsyncClient
from ReactTools import *

# Fetch statistics using the Roblox Asset ID (e.g., Valkyrie Helm)

class AgentState(TypedDict):
     messages:Annotated[Sequence[BaseMessage], add_messages]



#item = rolimons.item(1365767)

async def rolimonExtractor(itemID):
     item = rolimons.item(itemID)
     
     print(f"Item RAP: {item.rap}")
     print(f"Item Value: {item.value}")

# Get recent sales historical data for the item
     sales = item.get_recent_sales()
     times_list = []
     old_RAP_list = []
     new_RAP_list = []

     for sale in sales:
    
          utc_datetime = datetime.fromtimestamp(sale.timestamp, tz=timezone.utc)
          print(f"Time: {utc_datetime} | Old RAP: {sale.old_rap} -> New RAP: {sale.new_rap}")
          times_list.append(utc_datetime)
          old_RAP_list.append(sale.old_rap)
          new_RAP_list.append(sale.new_rap)
     dataset = {"old_rap":old_RAP_list, "new_rap":new_RAP_list}
     dataframe = pd.DataFrame(dataset)
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
    {dataframe.describe().to_markdown()}. Ensure your summary is between 100-150 words.""",
    
    options={
        "temperature": 0.0,  # Keeps the RAM cache small and fast
        "num_thread": 8  # Prevents hyper-thread traffic jams on your Ryzen 7
    } # Absolute zero completely turns off creative guessing
)
     
     return [old_RAP_list, new_RAP_list, times_list, response["response"]]
#plot_lists_directly(times_list, old_RAP_list, new_RAP_list)



