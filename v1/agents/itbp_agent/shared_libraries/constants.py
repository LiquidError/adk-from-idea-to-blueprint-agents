"""Constants used as keys into ADK's session state for ITBP agents."""

# System constants
SYSTEM_TIME = "_time"
ITBP_INITIALIZED = "_itbp_initialized"
ITBP_KEY = "itbp_config"

# Phase constants
CURRENT_PHASE = "current_phase"
PENDING_USER_ACTION = "pending_user_action"
PHASE_HISTORY = "phase_history"

# User input constants
USER_INPUT_IDEA = "user_input_idea"

# Analyst agent output constants
ANALYST_BRAINSTORMING_SUMMARY_MD = "analyst_brainstorming_summary_md"
ANALYST_RESEARCH_PROMPT_DRAFT_MD = "analyst_research_prompt_draft_md"
ANALYST_RESEARCH_FINDINGS_MD = "analyst_research_findings_md"
PROJECT_BRIEF_DRAFT_MD = "project_brief_draft_md"
PROJECT_BRIEF_MD = "project_brief_md"

# PM agent output constants
PRD_DRAFT_MD = "prd_draft_md"
PRD_MD = "prd_md"
EPICS_DRAFT_MD = "epics_draft_md"
EPICS_MD = "epics_md"

# Architect agent output constants
ARCHITECTURE_DOCS_DRAFT_MD = "architecture_docs_draft_md"
ARCHITECTURE_DOCS_MD = "architecture_docs_md"

# POSM agent output constants
POSM_PO_VALIDATION_SUMMARY_MD = "posm_po_validation_summary_md"
ALL_STORIES_DRAFT_MD = "all_stories_draft_md"
ALL_STORIES_MD = "all_stories_md"

# User feedback constants
USER_FEEDBACK_CONTENT = "user_feedback_content"
LAST_AGENT_OUTPUT = "last_agent_output"
