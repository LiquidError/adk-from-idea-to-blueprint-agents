"""Common data schema and types for ITBP (Idea-to-Blueprint-Pipeline) agents."""

from typing import Optional, List, Dict, Any, Union
from enum import Enum

from google.genai import types
from pydantic import BaseModel, Field


# Convenient declaration for controlled generation.
json_response_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)


class Phase(str, Enum):
    """Valid workflow phases for the orchestrator."""
    START = "START"
    GET_IDEA = "GET_IDEA"
    ANALYST_BRAINSTORM = "ANALYST_BRAINSTORM"
    ANALYST_RESEARCH_PROMPT_REVIEW = "ANALYST_RESEARCH_PROMPT_REVIEW"
    ANALYST_RESEARCH = "ANALYST_RESEARCH"
    ANALYST_BRIEF = "ANALYST_BRIEF"
    PM_DEFINE = "PM_DEFINE"
    ARCHITECT_DESIGN = "ARCHITECT_DESIGN"
    POSM_VALIDATE = "POSM_VALIDATE"
    POSM_STORIES = "POSM_STORIES"
    FINISHED = "FINISHED"


class UserAction(str, Enum):
    """Valid user actions that may be pending."""
    PROVIDE_IDEA = "PROVIDE_IDEA"
    REVIEW_BRAINSTORMING = "REVIEW_BRAINSTORMING"
    REVIEW_RESEARCH_PROMPT = "REVIEW_RESEARCH_PROMPT"
    REVIEW_RESEARCH = "REVIEW_RESEARCH"
    REVIEW_PROJECT_BRIEF = "REVIEW_PROJECT_BRIEF"
    REVIEW_PRD = "REVIEW_PRD"
    REVIEW_EPICS = "REVIEW_EPICS"
    REVIEW_ARCHITECTURE = "REVIEW_ARCHITECTURE"
    REVIEW_VALIDATION = "REVIEW_VALIDATION"
    REVIEW_STORIES = "REVIEW_STORIES"
    PROVIDE_FEEDBACK = "PROVIDE_FEEDBACK"


class BrainstormingSummary(BaseModel):
    """Brainstorming summary output from the Analyst Agent."""
    summary: str = Field(description="Summary of the brainstorming session")
    key_insights: List[str] = Field(description="Key insights from the brainstorming")
    potential_directions: List[str] = Field(description="Potential directions to explore")
    recommended_next_steps: List[str] = Field(description="Recommended next steps")


class ResearchPrompt(BaseModel):
    """Research prompt created by the Analyst Agent."""
    prompt: str = Field(description="The research prompt to be used")
    key_questions: List[str] = Field(description="Key questions to be answered")
    search_terms: List[str] = Field(description="Suggested search terms")


class ResearchFindings(BaseModel):
    """Research findings from the Analyst Agent."""
    summary: str = Field(description="Summary of the research findings")
    key_findings: List[str] = Field(description="Key findings from the research")
    market_analysis: str = Field(description="Analysis of the market")
    competitor_analysis: str = Field(description="Analysis of competitors")
    user_needs: List[str] = Field(description="Identified user needs")
    opportunities: List[str] = Field(description="Identified opportunities")
    challenges: List[str] = Field(description="Identified challenges")


class ProjectBrief(BaseModel):
    """Project brief created by the Analyst Agent."""
    title: str = Field(description="Project title")
    overview: str = Field(description="Brief overview of the project")
    problem_statement: str = Field(description="Statement of the problem being solved")
    target_audience: str = Field(description="Description of the target audience")
    goals_and_objectives: List[str] = Field(description="Project goals and objectives")
    success_criteria: List[str] = Field(description="Success criteria for the project")
    constraints: List[str] = Field(description="Project constraints")
    timeline: str = Field(description="Estimated timeline")
    resources: List[str] = Field(description="Required resources")
    stakeholders: List[str] = Field(description="Project stakeholders")


class Feature(BaseModel):
    """A feature in the PRD."""
    id: str = Field(description="Unique identifier for the feature")
    name: str = Field(description="Name of the feature")
    description: str = Field(description="Description of the feature")
    user_stories: List[str] = Field(description="User stories related to this feature")
    acceptance_criteria: List[str] = Field(description="Acceptance criteria for this feature")
    priority: str = Field(description="Priority of the feature (High, Medium, Low)")


class PRD(BaseModel):
    """Product Requirements Document created by the PM Agent."""
    title: str = Field(description="PRD title")
    version: str = Field(description="PRD version")
    overview: str = Field(description="Brief overview of the product")
    goals: List[str] = Field(description="Product goals")
    target_users: List[str] = Field(description="Target users")
    user_personas: List[Dict[str, Any]] = Field(description="User personas")
    features: List[Feature] = Field(description="Product features")
    non_functional_requirements: List[str] = Field(description="Non-functional requirements")
    assumptions: List[str] = Field(description="Assumptions made")
    constraints: List[str] = Field(description="Product constraints")
    out_of_scope: List[str] = Field(description="Features that are out of scope")


class Epic(BaseModel):
    """An epic in the product backlog."""
    id: str = Field(description="Unique identifier for the epic")
    title: str = Field(description="Title of the epic")
    description: str = Field(description="Description of the epic")
    user_value: str = Field(description="Value to the user")
    acceptance_criteria: List[str] = Field(description="Acceptance criteria for this epic")
    dependencies: List[str] = Field(description="Dependencies on other epics")
    priority: str = Field(description="Priority of the epic (High, Medium, Low)")
    estimated_effort: str = Field(description="Estimated effort")


class Epics(BaseModel):
    """Collection of epics created by the PM Agent."""
    epics: List[Epic] = Field(description="List of epics")
    release_plan: str = Field(description="High-level release plan")


class ArchitectureComponent(BaseModel):
    """A component in the architecture."""
    name: str = Field(description="Name of the component")
    description: str = Field(description="Description of the component")
    responsibilities: List[str] = Field(description="Responsibilities of the component")
    interfaces: List[str] = Field(description="Interfaces provided by the component")
    dependencies: List[str] = Field(description="Dependencies on other components")


class ArchitectureDocumentation(BaseModel):
    """Architecture documentation created by the Architect Agent."""
    overview: str = Field(description="Overview of the architecture")
    principles: List[str] = Field(description="Architectural principles")
    components: List[ArchitectureComponent] = Field(description="Components of the architecture")
    data_model: str = Field(description="Description of the data model")
    deployment_model: str = Field(description="Description of the deployment model")
    security_considerations: List[str] = Field(description="Security considerations")
    performance_considerations: List[str] = Field(description="Performance considerations")
    scalability_considerations: List[str] = Field(description="Scalability considerations")
    technology_stack: List[str] = Field(description="Technology stack")


class ValidationSummary(BaseModel):
    """Validation summary created by the POSM Agent."""
    is_valid: bool = Field(description="Whether the plan is valid")
    strengths: List[str] = Field(description="Strengths of the plan")
    concerns: List[str] = Field(description="Concerns about the plan")
    recommendations: List[str] = Field(description="Recommendations for improvement")
    go_no_go_decision: str = Field(description="Go/No-Go decision")
    rationale: str = Field(description="Rationale for the decision")


class UserStory(BaseModel):
    """A user story created by the POSM Agent."""
    id: str = Field(description="Unique identifier for the story")
    epic_id: str = Field(description="ID of the epic this story belongs to")
    title: str = Field(description="Title of the story")
    description: str = Field(description="Description in the form 'As a... I want to... So that...'")
    acceptance_criteria: List[str] = Field(description="Acceptance criteria for this story")
    priority: str = Field(description="Priority of the story (High, Medium, Low)")
    estimated_effort: str = Field(description="Estimated effort in story points")
    dependencies: List[str] = Field(description="Dependencies on other stories")


class UserStories(BaseModel):
    """Collection of user stories created by the POSM Agent."""
    stories: List[UserStory] = Field(description="List of user stories")
    sprint_plan: str = Field(description="High-level sprint plan")
