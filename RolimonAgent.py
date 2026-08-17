import rolimons
from datetime import datetime
from datetime import timezone
import pandas as pd
from ollama import AsyncClient
from ReactTools import *



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
     
     
     
     return [old_RAP_list, new_RAP_list, times_list, dataframe.describe()]




