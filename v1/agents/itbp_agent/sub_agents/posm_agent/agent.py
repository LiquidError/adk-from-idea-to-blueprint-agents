"""
Product Owner/Scrum Master (PO/SM) Agent Module

This module defines the PO/SM Agent, which is responsible for:
1. Validating the PRD, Epics, and Architecture documents from a product perspective
2. Providing a Go/No-Go decision based on standardized checklists
3. Generating detailed user stories based on the approved plan
4. Ensuring stories meet quality standards through checklists

The PO/SM Agent is the final agent in the workflow and transforms the technical
architecture into actionable user stories for implementation.
"""
from google.adk.agents import Agent
from .prompts_posm import get_posm_master_instructions
from ...tools.memory import memorize, update_phase
from ...shared_libraries.types import ValidationSummary, UserStories, json_response_config

# Import templates
from .prompts_posm import get_po_checklist_markdown, get_story_template_markdown

# Create sub-agents for specific tasks
validation_agent = Agent(
    name="validation_agent",
    model="gemini-2.5-pro-preview-05-06",
    description="Expert at validating product plans and documentation",
    instruction=f"""Validate the PRD, Epics, and Architecture documents and provide a Go/No-Go decision.

Use the following checklist as a guide:

{get_po_checklist_markdown()}
    """,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=ValidationSummary,
    output_key="posm_po_validation_summary_md",
    generate_content_config=json_response_config,
)

stories_agent = Agent(
    name="stories_agent",
    model="gemini-2.5-pro-preview-05-06",
    description="Expert at creating detailed user stories",
    instruction=f"""Create detailed user stories based on the approved plan.

Use the following template as a guide:

{get_story_template_markdown()}
    """,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=UserStories,
    output_key="all_stories_md",
    generate_content_config=json_response_config,
)

# Main POSM agent
posm_agent = Agent(
    name="posm_agent",
    model="gemini-2.5-pro-preview-05-06", # Needs to handle detailed document cross-referencing
    description="Technical Scrum Master / PO for validating plans and generating detailed developer stories.",
    instruction=get_posm_master_instructions(),
    tools=[memorize, update_phase],
    sub_agents=[validation_agent, stories_agent]
)