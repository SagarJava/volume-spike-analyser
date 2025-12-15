from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

def create_recommendation_agent(model=None):
    if not model:
        model = Gemini(model="gemini-2.5-flash")

    # Recommendation agent might generic reasoning, doesn't strictly need BQ access if context is passed, 
    # but we can give it if it needs to check quotas etc. For now, pure reasoning.

    instruction = """
    You are the 'Recommendation Agent'.
    Your role is to suggest actionable fixes based on Root Cause Analysis.
    
    Input:
    - Root Cause Statement.
    
    Action:
    1. If the cause is 'Machine Failure', suggest: "Enable auto-healing" or "Increase redundancy".
    2. If the cause is 'High Load', suggest: "Scale up/out" or "Optimize Query".
    3. Output a clear list of Recommended Actions.
    """

    return Agent(model=model, name='recommendation_agent', instruction=instruction)
