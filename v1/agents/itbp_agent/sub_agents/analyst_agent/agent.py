"""
Analyst Agent Module

This module defines the Analyst Agent, which is responsible for:
1. Facilitating brainstorming sessions to explore and refine ideas
2. Conducting market research using the Search Agent
3. Creating structured Project Briefs based on research and brainstorming

The Analyst Agent is the first agent in the workflow and sets the foundation
for the entire project by defining the problem space and initial requirements.
"""

from google.adk.agents import Agent
from .prompts_analyst import get_analyst_master_instructions, get_project_brief_template_markdown
from ..search_agent.agent import search_agent
from ...tools.memory import memorize
from ...shared_libraries.types import ProjectBrief, BrainstormingSummary, ResearchPrompt, ResearchFindings, json_response_config
from google.adk.tools.agent_tool import AgentTool


search_agent_as_tool = AgentTool(agent=search_agent)

# Import project brief template
from .prompts_analyst import get_project_brief_template_markdown

# Create sub-agents for specific tasks
brainstorming_agent = Agent(
    name="brainstorming_agent",
    model="gemini-2.5-pro-preview-05-06",
    description="Expert at brainstorming and exploring ideas",
    instruction="Generate a comprehensive brainstorming summary based on the user's idea.",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=BrainstormingSummary,
    output_key="analyst_brainstorming_summary_md",
    generate_content_config=json_response_config,
)

research_prompt_agent = Agent(
    name="research_prompt_agent",
    model="gemini-2.5-pro-preview-05-06",
    description="Expert at creating research prompts",
    instruction="Create a research prompt based on the brainstorming summary.",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=ResearchPrompt,
    output_key="analyst_research_prompt_draft_md",
    generate_content_config=json_response_config,
)

research_findings_agent = Agent(
    name="research_findings_agent",
    model="gemini-2.5-pro-preview-05-06",
    description="Expert at analyzing research findings",
    instruction="Analyze research findings and create a structured summary.",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=ResearchFindings,
    output_key="analyst_research_findings_md",
    generate_content_config=json_response_config,
)

project_brief_agent = Agent(
    name="project_brief_agent",
    model="gemini-2.5-pro-preview-05-06",
    description="Expert at creating project briefs",
    instruction=f"""Create a comprehensive project brief based on the research findings.

Use the following template as a guide:

{get_project_brief_template_markdown()}
    """,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=ProjectBrief,
    output_key="project_brief_md",
    generate_content_config=json_response_config,
)

# Main analyst agent that coordinates the sub-agents
analyst_agent = Agent(
    name="analyst_agent",
    model="gemini-2.5-pro-preview-05-06", # Or your preferred model for complex tasks
    description="Expert Market & Business Analyst for research, brainstorming, and project brief creation.",
    instruction=get_analyst_master_instructions(),
    tools=[
        memorize,
        search_agent_as_tool
    ],
    sub_agents=[
        brainstorming_agent,
        research_prompt_agent,
        research_findings_agent,
        project_brief_agent
    ],
)