from google.adk.tools.google_search_tool import google_search
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import FunctionTool
from datetime import datetime
from google.adk.agents import Agent


def hello(name: str) -> str:
    """
    Says hello to the user with the current date and time.
    """
    return f"Hello {name}! Current date and time is {datetime.now()}"

hello_func=FunctionTool(func=hello)

hello_agent=Agent(
    model="gemini-2.5-flash",
    name="hello_agent",
    description="A helpful assistant for user questions.",
    instruction="Answer user questions to the best of your knowledge",
    tools=[hello_func]
)

search_agent=Agent(
    model="gemini-2.5-flash",
    name="search_agent",
    description="A helpful assistant for user questions.",
    instruction="Answer user questions to the best of your knowledge",
    tools=[google_search]
)

hello_tool=AgentTool(agent=hello_agent)
search_tool=AgentTool(agent=search_agent)