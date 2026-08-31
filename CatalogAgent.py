import httpx
from ReactTools import *
from EconomyAgent import EconomyInfo
import asyncio
from ConsolidatorAgent import Analyser
from RolimonAgent import rolimonExtractor
from AssetIDreturner import get_limited_id
from ThumbNailAgent import download_limited_item_png
from Plotter import PlotRAPGraph, PlotVolumeGraph

class AgentState(TypedDict):
    messages:Annotated[Sequence[BaseMessage], add_messages]



@tool
async def catalogAgent(search_term: str):
    """Returns the asset id for a specific item"""

    
    

              
    print("Hi")
    rolimon, economy =  await asyncio.to_thread(rolimonExtractor, get_limited_id(search_term)), await EconomyInfo(get_limited_id(search_term))
                
    PlotRAPGraph(economy[0], rolimon[2], rolimon[0], rolimon[1], search_term)
    print("Done")
    PlotVolumeGraph(economy[1], economy[2], search_term)
    response = await download_limited_item_png(get_limited_id(search_term), search_term+".png")
                
    print("Plotted")
    if response:
            print(Analyser(rolimon[-1], economy[-1], search_term))
    return [rolimon, economy]


 
    

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
print(asyncio.run(Runner(input("Enter the item you want to know about: "))))


