import httpx
from ReactTools import *
from EconomyAgent import EconomyInfo
import asyncio
from ConsolidatorAgent import Analyser
from RolimonAgent import rolimonExtractor
from ThumbNailAgent import download_limited_item_png
from Plotter import PlotRAPGraph, PlotVolumeGraph

class AgentState(TypedDict):
    messages:Annotated[Sequence[BaseMessage], add_messages]



@tool
async def catalogAgent(search_term: str):
    """Returns the asset id for a specific item"""
    url = "https://catalog.roblox.com/v1/search/items/details"
    search_term = search_term
    # Keyword matches the search; Limit=10 is the lowest Roblox accepts,
    # but we will manually slice out the first result inside the code.
    params = {
        "keyword": search_term,
        "limit": 10,
        "salesTypeFilter": 2,     # 2 = Strictly targets Limiteds & Limited Uniques
        "sortType": 0,            # 0 = Relevance / default sorting
        # REMOVED CreatorTargetId to ensure we find items moved to the 'Roblox Presents' group
        # REMOVED CreatorType since we aren't filtering by creator anymore
        "includeNotForSale": True # True = Crucial for Limiteds that are no longer actively on-sale by Roblox
    }
    client = httpx.AsyncClient()
    response = await client.get(url, params=params)
    await client.aclose()
    print(response.status_code)
    
    # Check for HTTP status errors (like 429 rate limits or 400 bad requests)
    if response.status_code == 200:
      
                collectable_item = response.json()["data"][0]["collectibleItemId"]
                name = response.json()["data"][0]["name"]
                id = response.json()["data"][0]["id"] # Parse down into a dictionary
                print(collectable_item, name, id)
                Assetreturner(collectable_item)
                Assetreturner(id)
                rolimon, economy = await asyncio.gather(rolimonExtractor(AssetReturned[1]), EconomyInfo(AssetReturned[0]))
                PlotRAPGraph(economy[0], rolimon[2], rolimon[0], rolimon[1], search_term)
                print("Done")
                PlotVolumeGraph(economy[1], economy[2], search_term)
                response = await download_limited_item_png(AssetReturned[1], search_term+".png")
                
                print("Plotted")
                if response:
                    print(Analyser(rolimon[-1], economy[-1], search_term))
        
        
            

        
       
    


AssetReturned = []
def Assetreturner(ID):
    global AssetReturned
    AssetReturned.append(ID)



            
    # Return None if the item doesn't exist or the API request fails
    

tools = [catalogAgent]
llm = ChatOllama(model = "llama3.2")
model = llm.bind_tools(tools = tools)
async def Agent(state:AgentState):
    system_prompt = SystemMessage("""You are an AI Agent designed to get an ID on a specific item the user asks for.""")
    all_messages = [system_prompt]+list(state["messages"])
    response = await model.ainvoke(all_messages)
    return {"messages":[response]}

def Looper(state:AgentState):
    message = state["messages"][-1]
    if message.tool_calls:
        return "continue"
    else:
        return "exit"
    

graph = StateGraph(AgentState)
graph.add_node("agent", Agent)
graph.set_entry_point("agent")
graph.add_node("tool", ToolNode(tools = tools))
graph.add_edge("agent", "tool")
graph.add_edge("tool", "__end__")
app = graph.compile()


async def streamwriter(stream):
    async for s in stream:
        if "tool" in s:
            message = s['tool']["messages"][-1]
        
            
            


async def Runner(prompt):
    response = app.astream(({"messages":["user",prompt]}))
    await streamwriter(response)
    


import asyncio
print(asyncio.run(Runner("Find out about the item named the Valkyrie helm")))


