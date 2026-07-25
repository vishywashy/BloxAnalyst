import httpx
from ReactTools import *
from EconomyAgent import EconomyInfo
import asyncio
from RolimonAgent import rolimonExtractor
from Plotter import PlotGraph

class AgentState(TypedDict):
    messages:Annotated[Sequence[BaseMessage], add_messages]




async def catalogAgent(search_term: str):
    """Returns the asset id for a specific item"""
    url = "https://catalog.roblox.com/v1/search/items/details"
    
    # Keyword matches the search; Limit=10 is the lowest Roblox accepts,
    # but we will manually slice out the first result inside the code.
    params = {
        "keyword": search_term,
        "limit": 10,
        "salesTypeFilter": 1,  # 2 = Limiteds & Limited Uniques
              # 1 = Accessories (FIXED: Changing from 0 to 1 stops the NoneType error)
        "sortType": 0,         # 3 = Recently updated listings
        "CreatorTargetId": 1,  # 1 = Filters strictly for the official 'Roblox' account
        "CreatorType": 1,
        "includeNotForSale": True     # 1 = Specifies that the creator is a User account
    }
    client = httpx.AsyncClient()
    response = await client.get(url, params=params)
    
    # Check for HTTP status errors (like 429 rate limits or 400 bad requests)
    if response.status_code == 200:
        collectable_item = response.json()["data"][0]["collectibleItemId"]
        name = response.json()["data"][0]["name"]
        id = response.json()["data"][0]["id"] # Parse down into a dictionary
        print(collectable_item, name, id)
        Assetreturner(collectable_item)
        Assetreturner(id)
       
        
        
        rolimon, economy = await asyncio.gather(rolimonExtractor(AssetReturned[1]), EconomyInfo(AssetReturned[0]))
        print(rolimon, economy)
            
            
        PlotGraph(economy[0], rolimon[2], rolimon[0], rolimon[1], search_term)
            

        
        return "I don't know"
    


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
app = graph.compile()


async def streamwriter(stream):
    async for s in stream:
        if "tool" in s:
            message = s['tool']["messages"][-1]
            return message
            
            


async def Runner(prompt):
    response = app.astream(({"messages":["user",prompt]}))
    await streamwriter(response)
    


import asyncio
print(asyncio.run(Runner("Find out about Shaggy item")))


