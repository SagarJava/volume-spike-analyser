# from google.adk.agents import Agent
# from spike_analyser_agent.tools import hello_tool, search_tool
# from spike_analyser_agent.bq_tool import *


# # ---- Root Agent ----
# # root_agent = Agent(
# #     model="gemini-2.5-flash",
# #     name="spike_analyser_agent",
# #     description="A helpful assistant for user questions.",
# #     instruction="Answer user questions set to the best of your knowledge use the hello agent to say hello to some user and google_search to search the internet",
# #     tools=[hello_tool, search_tool],
# # )

# root_agent = Agent(
#     name="BigQuery_Agent",
#     model="gemini-2.5-flash",
#     description=(
#         "Agent to answer questions about BigQuery data and models and execute"
#         " SQL queries."
#     ),
#     instruction="""\
#         You are a data science agent with access to several BigQuery tools.
#         Make use of those tools to answer the user's questions.
#     """,
#     tools=[bigquery_toolset],
# )


import os
import google.auth
from google.adk.apps import App
from google.adk.plugins.bigquery_agent_analytics_plugin import BigQueryAgentAnalyticsPlugin, BigQueryLoggerConfig

from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.bigquery import BigQueryToolset, BigQueryCredentialsConfig
from google.adk.tools.bigquery.config import WriteMode
# Import specialized agents
from .agents.ingestor_agent import create_ingestor_agent
from .agents.spike_detector_agent import create_spike_detector_agent
from .agents.spike_detector_agent import create_correlation_agent
from .agents.rca_agent import create_rca_agent
from .agents.recommendation_agent import create_recommendation_agent
from .agents.trust_layer import TrustLayer
from google.adk.tools.bigquery.config import BigQueryToolConfig

# --- Configuration ---
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "ccibt-hack25ww7-718")
DATASET_ID = os.environ.get("BIG_QUERY_DATASET_ID", "718uc3demo")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "US")
GCS_BUCKET = os.environ.get("GCS_BUCKET_NAME")

# --- Environment Setup ---
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'
os.environ['GOOGLE_CLOUD_PROJECT'] = PROJECT_ID
os.environ['GOOGLE_CLOUD_LOCATION'] = LOCATION

def create_app():
    # 1. Plugin (Logging)
    bq_config = BigQueryLoggerConfig(
        enabled=True,
        gcs_bucket_name=GCS_BUCKET,
        log_multi_modal_content=True,
        max_content_length=500 * 1024,
        batch_size=1,
    )

    bq_logging_plugin = BigQueryAgentAnalyticsPlugin(
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        table_id="agent_events_v2",
        config=bq_config,
        location=LOCATION
    )

    tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)

    # 2. Shared Tools & Model
    credentials, _ = google.auth.default()
    
    bq_toolset = BigQueryToolset(
        credentials_config=BigQueryCredentialsConfig(credentials=credentials), bigquery_tool_config=tool_config
    )
    
    llm = Gemini(model="gemini-2.5-flash")

    # 3. Create Subagents
    # Each agent manages its own specific domain logic.
    ingestor = create_ingestor_agent(PROJECT_ID, DATASET_ID, tools=[bq_toolset], model=llm)
    spike_detector = create_spike_detector_agent(PROJECT_ID, DATASET_ID, tools=[bq_toolset], model=llm)
    correlation = create_correlation_agent(PROJECT_ID, DATASET_ID, tools=[bq_toolset], model=llm)
    # rca = create_rca_agent(PROJECT_ID, DATASET_ID, tools=[bq_toolset], model=llm)
    # recommendation = create_recommendation_agent(model=llm)

    # 4. Define Root Agent (Sequential Orchestrator)
    # Using SequentialAgent to enforce the strict pipeline order.
    # The output of one agent is passed as context to the next.
    
    root_agent = SequentialAgent(
        # model=llm,
        name='spike_analyser_agent',
        sub_agents=[
            ingestor,
            spike_detector,
            correlation,
            # rca,
            # recommendation
        ],
    )

    # 5. Create App
    app = App(
        name="spike_analyser_agent",
        root_agent=root_agent,
        # plugins=[bq_logging_plugin],
    )
    
    return app


# The ADK loader looks for a top-level 'app' or 'root_agent' variable.
app = create_app()
