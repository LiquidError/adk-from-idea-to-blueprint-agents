
"""The 'memorize' tool for ITBP agents to affect session states."""

from datetime import datetime
import json
import os
from typing import Dict, Any, Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext

from itbp_agent.shared_libraries import constants

CONFIG_PATH = os.getenv(
    "ITBP_CONFIG", os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "itbp_config.json")
)


def memorize_list(key: str, value: str, tool_context: ToolContext):
    """
    Memorize pieces of information.

    Args:
        key: the label indexing the memory to store the value.
        value: the information to be stored.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    mem_dict = tool_context.state
    if key not in mem_dict:
        mem_dict[key] = []
    if value not in mem_dict[key]:
        mem_dict[key].append(value)
    return {"status": f'Stored "{key}": "{value}"'}


def memorize(key: str, value: str, tool_context: ToolContext):
    """
    Memorize pieces of information, one key-value pair at a time.
    When the key is "current_phase", also updates PHASE_HISTORY and can set PENDING_USER_ACTION.

    Args:
        key: the label indexing the memory to store the value.
        value: the information to be stored.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    mem_dict = tool_context.state

    # Special handling for phase transitions
    if key == constants.CURRENT_PHASE:
        # Store the previous phase in history if it exists and is different
        if constants.CURRENT_PHASE in mem_dict and mem_dict[constants.CURRENT_PHASE] != value:
            if constants.PHASE_HISTORY not in mem_dict:
                mem_dict[constants.PHASE_HISTORY] = []
            if mem_dict[constants.CURRENT_PHASE] not in mem_dict[constants.PHASE_HISTORY]:
                mem_dict[constants.PHASE_HISTORY].append(mem_dict[constants.CURRENT_PHASE])

    # Store the value
    mem_dict[key] = value
    return {"status": f'Stored "{key}": "{value}"'}


def forget(key: str, value: str, tool_context: ToolContext):
    """
    Forget pieces of information.

    Args:
        key: the label indexing the memory to store the value.
        value: the information to be removed.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    if tool_context.state[key] is None:
        tool_context.state[key] = []
    if value in tool_context.state[key]:
        tool_context.state[key].remove(value)
    return {"status": f'Removed "{key}": "{value}"'}


def update_phase(phase: str, pending_action: Optional[str] = None, tool_context: ToolContext = None):
    """
    Update the current phase and related state variables.
    This function handles all phase transition state updates in one call.

    Args:
        phase: The new phase to transition to.
        pending_action: Optional pending user action to set.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    # Update current phase
    memorize(constants.CURRENT_PHASE, phase, tool_context)

    # Update pending user action if provided
    if pending_action is not None:
        memorize(constants.PENDING_USER_ACTION, pending_action, tool_context)

    return {
        "status": f"Transitioned to phase: {phase}" +
                 (f" with pending action: {pending_action}" if pending_action else "")
    }


def _set_initial_states(source: Dict[str, Any], target: State | dict[str, Any]):
    """
    Setting the initial session state given a JSON object of states.

    Args:
        source: A JSON object of states.
        target: The session state object to insert into.
    """
    if constants.SYSTEM_TIME not in target:
        target[constants.SYSTEM_TIME] = str(datetime.now())

    if constants.ITBP_INITIALIZED not in target:
        target[constants.ITBP_INITIALIZED] = True

        # Update with source data
        target.update(source)

        # Initialize phase information if not present
        if constants.CURRENT_PHASE not in target:
            target[constants.CURRENT_PHASE] = "START"

        if constants.PENDING_USER_ACTION not in target:
            target[constants.PENDING_USER_ACTION] = None

        if constants.PHASE_HISTORY not in target:
            target[constants.PHASE_HISTORY] = []

        # Initialize metadata
        if "_metadata" not in target:
            target["_metadata"] = {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "version": "1.0",
                "state_history": []
            }


def _load_precreated_config(callback_context: CallbackContext):
    """
    Sets up the initial state.
    Set this as a callback as before_agent_call of the root_agent.
    This gets called before the system instruction is constructed.

    Args:
        callback_context: The callback context.
    """
    data = {}
    with open(CONFIG_PATH, "r") as file:
        data = json.load(file)
        print(f"\nLoading Initial State: {data}\n")

    _set_initial_states(data["state"], callback_context.state)
