
"""
Main Orchestrator Agent Module

This module defines the main orchestrator agent that coordinates the workflow
between specialist sub-agents (Analyst, PM, Architect, PO/SM) and manages
the overall conversation with the user.

The orchestrator maintains session state, handles transitions between phases,
and ensures that the appropriate context is passed to each sub-agent.
"""

from google.adk.agents import Agent
from google.genai import types
from google.adk.agents.callback_context import CallbackContext

from itbp_agent import prompt
from itbp_agent.tools.memory import _load_precreated_config, memorize
from itbp_agent.shared_libraries.types import Phase
from itbp_agent.shared_libraries.constants import CURRENT_PHASE

from .sub_agents.analyst_agent.agent import analyst_agent
from .sub_agents.pm_agent.agent import pm_agent
from .sub_agents.architect_agent.agent import architect_agent
from .sub_agents.posm_agent.agent import posm_agent


# Configure the root agent with more flexibility to jump between phases
root_agent = Agent(
    model="gemini-2.5-pro-preview-05-06",
    name="itbp_agent",
    description="Orchestrates the Idea-to-Blueprint-Pipeline workflow between specialist sub-agents",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        analyst_agent,
        pm_agent,
        architect_agent,
        posm_agent,
    ],
    before_agent_callback=_load_precreated_config,  # Use our new handler that shows the greeting
    tools=[memorize],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.2,  # Lower temperature for more consistent orchestration
        top_p=0.95,
        top_k=40,
    ),
)