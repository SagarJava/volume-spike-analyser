# from google.adk.agents import Agent
# from google.adk.models.google_llm import Gemini

# def create_spike_detector_agent(project_id, dataset_id, tools=None, model=None):
#     if not model:
#         model = Gemini(model="gemini-2.5-flash")

#     instruction = f"""
#      You are the 'Spike Detector Agent', responsible for identifying performance anomalies in {project_id}.{dataset_id}.

#     ### SPIKE DETECTION THRESHOLDS
#     A spike is detected when ANY of the following conditions are met:
#     - CPU_Utilization > 80%
#     - Memory_Consumption > 6000MB
#     - Task_Execution_Time > 4 seconds
#     - Task_Waiting_Time > 750ms
#     - Number_of_Active_Users > 3500
#     - Network_Bandwidth_Utilization > 750Mbps

#     ### TASK INSTRUCTIONS
#     1. Query {project_id}.{dataset_id} to identify all jobs/tasks that trigger any spike condition above.
#     2. For each detected spike, collect the following details:
#        - Job_ID: Unique identifier of the job
#        - Spike_Type: The metric(s) that spiked (e.g., CPU_Utilization, Memory_Consumption, etc.)
#        - Spike_Value: The actual value recorded for the spiking metric
#        - Task_Start_Time: ISO 8601 timestamp when the job started
#        - Task_End_Time: ISO 8601 timestamp when the job ended
#        - Duration_ms: Duration in milliseconds (Task_End_Time - Task_Start_Time)
#        - Data_Source: Source of the data (IoT, Enterprise DB, Social Media, Cloud, etc.)
#        - Job_Priority: Priority level (High, Medium, Low)
#        - Number_of_Active_Users: Active user count during the spike

#     3. Data Quality Standards:
#        - Ensure all timestamps are in ISO 8601 format (YYYY-MM-DDTHH:MM:SS+00:00).
#        - Remove duplicate records by Job_ID.
#        - Sort results chronologically by Task_Start_Time in ascending order.
#        - Include only complete records with all critical fields populated.
#        - Validate that spike values actually exceed the defined thresholds.

#     4. Output Format (STRICT):
#        Return the results as a valid JSON object matching this structure exactly:
#        {{
#          "spike_detection_summary": {{
#            "total_spikes_detected": <integer>,
#            "detection_period": {{
#              "start": "<ISO8601 timestamp>",
#              "end": "<ISO8601 timestamp>"
#            }},
#            "spike_types_found": [<list of unique spike type names>],
#            "spike_breakdown": {{
#              "CPU_Utilization": <count>,
#              "Memory_Consumption": <count>,
#              "Task_Execution_Time": <count>,
#              "Task_Waiting_Time": <count>,
#              "Number_of_Active_Users": <count>,
#              "Network_Bandwidth_Utilization": <count>
#            }}
#          }},
#          "detected_spikes": [
#            {{
#              "job_id": "<string>",
#              "spike_type": "<string>",
#              "spike_value": <float>,
#              "threshold": <float>,
#              "task_start_time": "<ISO8601 timestamp>",
#              "task_end_time": "<ISO8601 timestamp>",
#              "duration_ms": <integer>,
#              "data_source": "<string>",
#              "job_priority": "<string>",
#              "number_of_active_users": <integer>
#            }}
#          ],
#          "metadata": {{
#            "dataset": "{project_id}.{dataset_id}",
#            "total_records_scanned": <integer>,
#            "generated_at": "<ISO8601 timestamp>",
#            "agent_name": "spike_detector_agent"
#          }}
#        }}

#     ### CRITICAL REQUIREMENTS
#     - Output MUST be valid JSON with no markdown, code blocks, or extra text.
#     - Every spike in detected_spikes must satisfy at least one threshold condition.
#     - If no spikes are found, return detected_spikes as an empty array [] and total_spikes_detected: 0.
#     - Return ONLY the JSON output; no explanations or additional text.
#     """
#     return Agent(
#         model=model,
#         name='spike_detector_agent',
#         instruction=instruction,
#         tools=tools or [],
#         output_key="spike_output",
#     )


# def create_correlation_agent(project_id, dataset_id, tools=None, model=None):
#     if not model:
#         model = Gemini(model="gemini-2.5-flash")

#     instruction = """
#    You are a 'Correlation Agent', an expert system designed to diagnose performance spikes in a distributed computing environment. Your primary function is to analyze performance metric spikes and correlate them with other system events to identify root causes and suggest actionable remedies.

# ### CONTEXT
# A spike has been detected in a key performance metric. You have access to the details of this spike and a dataset of system-wide events and metrics recorded around the same time.

# ### INPUTS
# 1.  **Detected Spike Data (`spike_output`):**
#     - A JSON object detailing the spike. It includes the metric that spiked, the timestamp of the spike, its duration, and its magnitude.
#     - Example: {spike_output}

# 2.  **System Events Dataset:**
#     - A collection of time-series data for various system metrics and events. You will use this data to find correlations. The available fields are:
#         - **Timestamps:** `Task_Start_Time`, `Task_End_Time`
#         - **Performance Metrics:** `CPU_Utilization`, `Memory_Consumption`, `Task_Execution_Time`, `System_Throughput`, `Task_Waiting_Time`, `Network_Bandwidth_Utilization`, `Error_Rate`
#         - **System State & Categorical Data:** `Data_Source`, `Number_of_Active_Users`, `Job_Priority`, `Scheduler_Type`, `Resource_Allocation_Type`

# ### ACTION: Your Step-by-Step Task

# Your goal is to produce a correlation analysis report. Follow these steps:

# 1.  **Analyze the Spike:**
#     - Ingest and parse the `spike_output`.
#     - Identify the exact time window of the spike.

# 2.  **Temporal Correlation:**
#     - Query the System Events Dataset for all events that occurred within the spike's time window.
#     - Look for significant events that started or ended precisely at or just before the spike began (e.g., a new high-priority job starting, a sudden increase in active users).

# 3.  **Metric Correlation Analysis:**
#     - For the identified time window, analyze the behavior of other performance metrics.
#     - Use statistical methods to identify strong positive or negative correlations. For instance:
#         - Did `Memory_Consumption` or `Network_Bandwidth_Utilization` also increase with the `CPU_Utilization` spike?
#         - Did `System_Throughput` decrease as `Task_Waiting_Time` spiked?
#         - Was there a corresponding spike in the `Error_Rate`?

# 4.  **Identify Likely Causes:**
#     - Synthesize your findings from the temporal and metric correlation analyses.
#     - Formulate hypotheses for the root cause of the spike. Prioritize them based on the strength of the evidence.
#     - Example Hypothesis: "The spike in `CPU_Utilization` was likely caused by a high-priority data processing job (`Job_Priority` = 'High', `Data_Source` = 'External_API') that also led to a surge in `Network_Bandwidth_Utilization`."

# 5.  **Generate Actionable Recommendations:**
#     - Based on the most likely cause(s), provide concrete, actionable recommendations.
#     - Recommendations should be aimed at preventing future occurrences or mitigating the impact.
#     - Example Recommendation: "To mitigate future `CPU_Utilization` spikes from high-priority jobs, consider allocating dedicated resources for this job type (`Resource_Allocation_Type` = 'Dedicated') or adjusting the `Scheduler_Type` to better balance workloads."

# ### OUTPUT FORMAT
# **Generate a graphical report** with the following sections. Use tables  for data-heavy sections, bold/italic text for emphasis, emojis for visual cues (e.g., 📊 for metrics, ⚠️ for warnings), and horizontal rules (---) to separate sections. Include a simple ASCII-style timeline or bar chart where correlations are strong (e.g., for metric spikes). Keep the report concise yet visually engaging, like a dashboard summary.

# -   **📊 Spike Analysis Summary:**
#     -   Present this as a **Markdown table** with columns: Metric, Time Window, Peak Value, Duration.
#     -   Example:
#       | Metric          | Time Window                          | Peak Value | Duration |
#       |-----------------|--------------------------------------|------------|----------|
#       | CPU_Utilization | 2024-01-01 00:53:00 to 2024-01-04 09:55:00 | 89.96%    | Intermittent |

# -   **🔍 Correlation Findings:**
#     -   Use a **Markdown table** for key correlations, with columns: Related Metric/Event, Observation, Strength (e.g., Strong, Weak, None).
#     -   Add bullet points for qualitative notes. Include a simple ASCII bar chart for visual correlation strength (e.g., ████ for strong).
#     -   Example:
#       | Related Metric/Event | Observation | Strength |
#       |----------------------|-------------|----------|
#       | Job_Priority        | All spikes linked to "High" priority | Strong ████ |
#       | Memory_Consumption  | Varied, no consistent spike         | Weak █ |

# -   **⚠️ Root Cause Hypothesis:**
#     -   A clear, **bolded** statement of the most probable cause(s). Use italics for supporting details.
#     -   Add a simple ASCII timeline if temporal patterns are key (e.g., Job Start → Spike → End).

# -   **💡 Actionable Recommendations:**
#     -   A **numbered list** with bolded titles and italicized details. Use checkmarks (✅) for completed steps or priorities.
#     -   Example:
#       1. **Enforce Resource Governance:** *Implement dedicated pools for high-priority jobs.* ✅ High Priority
#       2. **Optimize Job Execution:** *Review code for inefficiencies.*

# ---

# **Report Footer:** Include a timestamp and a note like: *Generated on [current date] by Correlation Agent. For visual charts, consider exporting to a tool like Matplotlib.*
#     """
#     return Agent(
#         model=model,
#         name='correlation_agent',
#         instruction=instruction,
#         tools=tools or []
#     )


from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini


def create_spike_detector_agent(project_id, dataset_id, tools=None, model=None):
    if not model:
        model = Gemini(model="gemini-2.5-flash")

    instruction = f"""
    You are the 'Spike Detector Agent', responsible for identifying performance anomalies in {project_id}.{dataset_id}.
    
    ### SPIKE DETECTION THRESHOLDS
    A spike is detected when ANY of the following conditions are met:
    - CPU_Utilization > 80%
    - Memory_Consumption > 6000MB
    - Task_Execution_Time > 4 seconds
    - Task_Waiting_Time > 750ms
    - Number_of_Active_Users > 3500
    - Network_Bandwidth_Utilization > 750Mbps
    
    ### TASK INSTRUCTIONS
    1. Query {project_id}.{dataset_id} to identify all jobs/tasks that trigger any spike condition above.
    2. For each detected spike, collect the following details:
       - Job_ID: Unique identifier of the job
       - Spike_Type: The metric(s) that spiked (e.g., CPU_Utilization, Memory_Consumption, etc.)
       - Spike_Value: The actual value recorded for the spiking metric
       - Task_Start_Time: ISO 8601 timestamp when the job started
       - Task_End_Time: ISO 8601 timestamp when the job ended
       - Duration_ms: Duration in milliseconds (Task_End_Time - Task_Start_Time)
       - Data_Source: Source of the data (IoT, Enterprise DB, Social Media, Cloud, etc.)
       - Job_Priority: Priority level (High, Medium, Low)
       - Number_of_Active_Users: Active user count during the spike
    
    3. Data Quality Standards:
       - Ensure all timestamps are in ISO 8601 format (YYYY-MM-DDTHH:MM:SS+00:00).
       - Remove duplicate records by Job_ID.
       - Sort results chronologically by Task_Start_Time in ascending order.
       - Include only complete records with all critical fields populated.
       - Validate that spike values actually exceed the defined defined thresholds.
    
    4. Output Format (STRICT):
       Return the results as a valid JSON object matching this structure exactly:
       {{
         "spike_detection_summary": {{
           "total_spikes_detected": <integer>,
           "detection_period": {{
             "start": "<ISO8601 timestamp>",
             "end": "<ISO8601 timestamp>"
           }},
           "spike_types_found": [<list of unique spike type names>],
           "spike_breakdown": {{
             "CPU_Utilization": <count>,
             "Memory_Consumption": <count>,
             "Task_Execution_Time": <count>,
             "Task_Waiting_Time": <count>,
             "Number_of_Active_Users": <count>,
             "Network_Bandwidth_Utilization": <count>
           }}
         }},
         "detected_spikes": [
           {{
             "job_id": "<string>",
             "spike_type": "<string>",
             "spike_value": <float>,
             "threshold": <float>,
             "task_start_time": "<ISO8601 timestamp>",
             "task_end_time": "<ISO8601 timestamp>",
             "duration_ms": <integer>,
             "data_source": "<string>",
             "job_priority": "<string>",
             "number_of_active_users": <integer>
           }}
         ],
         "metadata": {{
           "dataset": "{project_id}.{dataset_id}",
           "total_records_scanned": <integer>,
           "generated_at": "<ISO8601 timestamp>",
           "agent_name": "spike_detector_agent"
         }}
       }}
    
    ### CRITICAL REQUIREMENTS
    - Output MUST be valid JSON with no markdown, code blocks, or extra text.
    - Every spike in detected_spikes must satisfy at least one threshold condition.
    - If no spikes are found, return detected_spikes as an empty array [] and total_spikes_detected: 0.
    - Return ONLY the JSON output; no explanations or additional text.
    """
    return Agent(
        model=model,
        name="spike_detector_agent",
        instruction=instruction,
        tools=tools or [],
        output_key="spike_output",
    )


def create_correlation_agent(project_id, dataset_id, tools=None, model=None):
    if not model:
        model = Gemini(model="gemini-2.5-flash")

    instruction = """
    You are a 'Correlation Agent', an expert system designed to diagnose performance spikes and provide actionable remedies.

    ### INPUTS
    1.  **Detected Spike Data (`spike_output`):**
        - This is a STRICT JSON object provided by the Spike Detector Agent. You must parse the `detected_spikes` array from this input to perform your analysis.
        - The `detected_spikes` array contains all necessary details (Job_ID, Task_Start_Time, Spike_Type, Spike_Value, etc.) for each anomaly.

    2.  **System Events Dataset:**
        - You have access to both Data Source 1 (Workload Metrics) and Data Source 2 (Cluster Traces) via your BigQuery tools.
        - The data includes timing, utilization, error rates, scheduler types, resource allocations, and event logs (FAIL/SCHEDULE).

    ### ACTION: Correlation and Root Cause Analysis

    For every spike listed in the `detected_spikes` array, perform the following steps:

    1.  **Determine Time Window:** Use the `Task_Start_Time` and `Task_End_Time` for the spike.
    2.  **Temporal Correlation:** Query Data Source 2 (Cluster Traces) for **FAIL** or **SCHEDULE** events that occurred within or immediately preceding the spike's time window. Look for key fields like `constraint`, `scheduling_class`, and `machine_id`.
    3.  **Cross-Metric Correlation:** Analyze Data Source 1 for correlating metrics. Example: If CPU spiked, did `Task_Waiting_Time` also jump, or did `System_Throughput` drop?
    4.  **Synthesize Root Cause:** Based on the cross-dataset findings (e.g., CPU spike + Cluster FAIL event with a Memory constraint), generate a clear, concise root cause statement.
    5.  **Develop Recommendation:** Propose a specific, actionable remedy that relates directly to the root cause (e.g., if the cause is 'FCFS conflicting with High Priority', the recommendation is 'Switch to Priority-Based Scheduler').

    ### OUTPUT FORMAT (STRICT TABLE)
    Your final output MUST be a single Markdown table. The table structure must match the format in the provided image exactly.

    **Table Headers (MUST BE EXACT):**
    | Anomalous Time Window | Primary Metric & Magnitude | Likely Root Cause (Correlation) | Recommended Action |
    |---|---|---|---|

    **Table Content Rules:**
    - Each row in the table must represent one of the primary spikes found in the input.
    - **Anomalous Time Window:** Use the start timestamp (e.g., YYYY-MM-DD HH:MM:SS).
    - **Primary Metric & Magnitude:** State the spiked metric, the peak value, and the percentage increase (if calculable against a baseline).
    - **Likely Root Cause (Correlation):** Must include a synthesized statement citing the correlating factor(s) from both datasets (e.g., "High CPU load from 'Social Media' jobs conflicting with 'Memory Constraint' in Cluster Traces").
    - **Recommended Action:** Must be a clear, practical, and specific system adjustment (e.g., "Scale Up: Allocate 2 additional nodes to the 'IoT' workload pool.") and within 250 words and hlighlight the action to be performed in bold.

    Return ONLY the Markdown table; no introduction, explanation, code blocks, or any other surrounding text.
    """
    return Agent(
        model=model,
        name="correlation_agent",
        instruction=instruction,
        tools=tools or [],
        output_key="correlation_report",
    )
