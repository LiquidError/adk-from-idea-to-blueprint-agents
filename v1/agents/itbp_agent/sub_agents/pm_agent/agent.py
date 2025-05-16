"""
Product Manager (PM) Agent Module

This module defines the PM Agent, which is responsible for:
1. Defining the MVP scope based on the Project Brief
2. Creating a detailed Product Requirements Document (PRD)
3. Structuring work into logical Epics with clear requirements
4. Providing guidance for the Architect in the form of an Initial Architect Prompt

The PM Agent takes the Project Brief from the Analyst Agent and transforms it
into structured requirements that will guide the technical implementation.
"""
from google.adk.agents import Agent
from .prompts_pm import get_pm_master_instructions
from ...tools.memory import memorize
from ...shared_libraries.types import PRD, Epics, json_response_config

# Import templates
from .prompts_pm import get_prd_template_markdown, get_epic_template_markdown

# Create sub-agents for specific tasks
prd_agent = Agent(
    name="prd_agent",
    model="gemini-2.5-pro-preview-05-06",
    description="Expert at creating Product Requirements Documents",
    instruction=f"""Create a comprehensive PRD based on the project brief.

Use the following template as a guide:

{get_prd_template_markdown()}
    """,    
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=PRD,
    output_key="prd_md",
    generate_content_config=json_response_config,
)

epics_agent = Agent(
    name="epics_agent",
    model="gemini-2.5-pro-preview-05-06",
    description="Expert at creating Epics and structuring work",
    instruction=f"""Create a set of epics based on the PRD.

Use the following template as a guide:

{get_epic_template_markdown()}
    """,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=Epics,
    output_key="epics_md",
    generate_content_config=json_response_config,
)

# Main PM agent that coordinates the sub-agents
pm_agent = Agent(
    name="pm_agent",
    model="gemini-2.5-pro-preview-05-06", # Capable model for document generation
    description="Expert Product Manager for creating PRDs, Epics, and defining MVP scope.",
    instruction=get_pm_master_instructions(),
    tools=[memorize],
    sub_agents=[prd_agent, epics_agent]
)
