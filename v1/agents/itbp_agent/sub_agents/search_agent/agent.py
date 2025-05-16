"""
Search Agent Module

This module defines the Search Agent, which is responsible for:
1. Providing factual, up-to-date information through Google Search
2. Conducting deep research on product development topics
3. Supporting the Analyst Agent with market research and competitive analysis

The Search Agent serves as a research assistant to the other agents,
particularly the Analyst Agent, by providing grounded information from
external sources.
"""

from google.adk.agents import Agent
from ...tools.deep_research import deep_research_tool
from .prompts_search import (
    get_search_master_instructions,
)


search_agent = Agent(
    model="gemini-2.0-flash-001",
    name="search_agent",
    description="An agent providing deep research via Tavily for the Idea-to-Blueprint-Pipeline framework.",
    instruction=get_search_master_instructions(),
    tools=[
        deep_research_tool
    ],
)
