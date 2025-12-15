from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

def create_rca_agent(project_id, dataset_id, tools=None, model=None):
    if not model:
        model = Gemini(model="gemini-2.5-flash")
    
    instruction = f"""
    You are the 'Root Cause Analyzer (RCA) Agent'.
    Your role is to explain WHY a problem happened.
    
    Input:
    - Correlated data (Job Spike + Machine Failure).
    
    Action:
    1. Analyze the relationship. Did the machine failure cause the spike (retry storm)? Or did the spike cause the failure (OOM)?
    2. Use your knowledge of distributed systems to formulate a hypothesis.
    3. Output a detailed Root Cause Statement.
    """
    return Agent(model=model, name='rca_agent', instruction=instruction, tools=tools or [])
