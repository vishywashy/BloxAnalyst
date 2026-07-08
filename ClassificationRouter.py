from pydantic import BaseModel
import ollama
from typing import Literal
class AgentRouter(BaseModel):
    Agent:Literal["TradeRoute", "PlayerInfoRoute", "NewsRoute"]


purpose = input("What task are you using this agent for: ")
prompt = input("Type your message here: ")


AgentToCall = AgentRouter.model_validate_json(ollama.generate(model = "llama3.2", prompt = purpose, format=AgentRouter.model_json_schema())["response"]).Agent
