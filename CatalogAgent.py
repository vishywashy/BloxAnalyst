import httpx
from ReactTools import *

class AgentState(TypedDict):
    messages:Annotated[Sequence[BaseMessage], add_messages]



@tool
async def catalogAgent(search_term: str):
    """Returns the asset id for a specific item"""
    url = "https://catalog.roblox.com/v1/search/items/details"
    
    # Keyword matches the search; Limit=10 is the lowest Roblox accepts,
    # but we will manually slice out the first result inside the code.
    params = {
        "keyword": search_term,
        "Limit": 10 
    }
    client = httpx.AsyncClient()
    response = await client.get(url, params=params)
    
    # Check for HTTP status errors (like 429 rate limits or 400 bad requests)
    if response.status_code == 200:
        data = response.json() # Parse down into a dictionary
        results_list = data.get("data", [])
        
        if results_list:
            # Index [0] pulls the first matching dictionary object from the array
            first_item = results_list[0] 
            Assetreturner(first_item["id"])
            return "Execution complete"

        
        return None
    

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
            message = s["tool"]["messages"][-1]
            return message
            
            


async def Runner():
    response = app.astream(({"messages":["user", "Find out about the valkyrie helm"]}))
    await streamwriter(response)
    return AssetReturned[-1]


import asyncio
print(asyncio.run(Runner()))
    


