from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

def create_ingestor_agent(project_id, dataset_id, tools=None, model=None):
    if not model:
        model = Gemini(model="gemini-2.5-flash")
    
    instruction = f"""
    You are the 'Data Ingestor Agent'.
    Your role is to verify that the necessary data is available in BigQuery datasetn project id = {project_id} and dataset id = {dataset_id}.
    
    Tables required:
    `cloud_workload_dataset`
    
    Action:
    1. Query the `__TABLES__` view or try to select 1 row from each table.
    2. If tables exist and have data, report "HEALTHY".
    3. If not, report "MISSING DATA".
    """
    return Agent(
        model=model,
        name='ingestor_agent',
        instruction=instruction, 
        tools=tools or []
    )

