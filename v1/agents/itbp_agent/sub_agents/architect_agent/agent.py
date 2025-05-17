"""
Architect Agent Module

This module defines the Architect Agent, which is responsible for:
1. Designing the technical architecture based on the PRD and Epics
2. Creating comprehensive architecture documentation
3. Validating the architecture against standardized checklists
4. Enriching Epics with technical implementation details

The Architect Agent takes the PRD and Epics from the PM Agent and transforms them
into a detailed technical design that will guide the implementation.
"""

from google.adk.agents import Agent
from .prompts_architect import get_architect_master_instructions
from ...tools.memory import memorize, update_phase
from ...shared_libraries.types import ArchitectureDocumentation, json_response_config


# Import architecture templates
from .prompts_architect import (
    get_master_architecture_template_markdown,
    get_coding_standards_template_markdown,
    get_data_models_template_markdown,
    get_environment_vars_template_markdown,
    get_project_structure_template_markdown
)

# Create architecture documentation agent
architecture_docs_agent = Agent(
    name="architecture_docs_agent",
    model="gemini-2.5-pro-preview-05-06",
    description="Expert at creating comprehensive architecture documentation",
    instruction=f"""Create detailed architecture documentation based on the PRD and Epics.

Use the following templates as a guide:

Master Architecture Template:
{get_master_architecture_template_markdown()}

Coding Standards Template:
{get_coding_standards_template_markdown()}

Data Models Template:
{get_data_models_template_markdown()}

Environment Variables Template:
{get_environment_vars_template_markdown()}

Project Structure Template:
{get_project_structure_template_markdown()}
    """,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=ArchitectureDocumentation,
    output_key="architecture_docs_md",
    generate_content_config=json_response_config,
)

# Main architect agent
architect_agent = Agent(
    name="architect_agent",
    model="gemini-2.5-pro-preview-05-06", # Needs strong reasoning for technical design
    description="Expert Solution/Software Architect for designing technical architecture and creating related documentation.",
    instruction=get_architect_master_instructions(),
    tools=[memorize, update_phase],
    sub_agents=[architecture_docs_agent]
)