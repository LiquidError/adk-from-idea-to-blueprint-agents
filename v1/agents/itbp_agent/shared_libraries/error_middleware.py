"""
Error Handling Middleware Module

This module provides middleware for handling errors in the orchestrator agent.
It includes:

1. Error handling middleware for agent callbacks
2. Error handling middleware for tool functions
3. Graceful degradation for non-critical failures
4. User-friendly error message generation
"""

import logging
import functools
import traceback
import asyncio
from typing import Dict, Any, Optional, Callable, TypeVar, Union, List, Tuple, Type
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import ToolContext

from .logging_config import get_logger, ErrorCategory
from .error_handling import (
    ITBPMethodError,
    create_user_error_message,
    classify_exception
)

# Get module logger
logger = get_logger(__name__)

# Function type for type hints
F = TypeVar('F', bound=Callable[..., Any])
AsyncF = TypeVar('AsyncF', bound=Callable[..., Any])

# --- Callback Error Handling Middleware ---

def handle_callback_errors(func: AsyncF) -> AsyncF:
    """
    Decorator to handle errors in agent callbacks.

    Args:
        func: The callback function to wrap

    Returns:
        Wrapped callback function
    """
    @functools.wraps(func)
    async def wrapper(callback_context: CallbackContext):
        try:
            # Get session ID from state if available
            session_id = callback_context.state.get("_session_id", "unknown")
            phase = callback_context.state.get("current_phase", "unknown")

            # Create a logger with session context
            ctx_logger = get_logger(__name__, session_id=session_id, phase=phase)
            ctx_logger.info(f"Executing callback: {func.__name__}")

            # Execute the callback
            await func(callback_context)

            ctx_logger.info(f"Callback {func.__name__} completed successfully")

        except Exception as e:
            # Log the error with context
            error_category = classify_exception(e)
            logger.error(
                f"Error in callback {func.__name__}: {type(e).__name__}: {str(e)}",
                exc_info=True,
                extra={"error_category": error_category.name, "session_id": session_id, "phase": phase}
            )

            # Create user-friendly error message
            user_message = create_user_error_message(e)

            # Set error response for the user
            error_response = (
                f"I encountered an issue while processing your request. {user_message}\n\n"
                f"Please try again or contact support if the issue persists."
            )

            # Set the agent response to the error message
            callback_context.set_agent_response(error_response)

            # Don't re-raise the exception to allow the agent to continue

    return wrapper

# --- Tool Error Handling Middleware ---

def handle_tool_errors(func: AsyncF) -> AsyncF:
    """
    Decorator to handle errors in tool functions.

    Args:
        func: The tool function to wrap

    Returns:
        Wrapped tool function
    """
    @functools.wraps(func)
    async def wrapper(**kwargs):
        try:
            # Extract tool_context from kwargs
            tool_context = kwargs.get('tool_context')

            # Get session ID from state if available
            session_id = tool_context.state.get("_session_id", "unknown") if tool_context else "unknown"
            phase = tool_context.state.get("current_phase", "unknown") if tool_context else "unknown"

            # Create a logger with session context
            ctx_logger = get_logger(__name__, session_id=session_id, phase=phase)
            ctx_logger.info(f"Executing tool: {func.__name__} with kwargs: {kwargs}")

            # Execute the tool function
            result = await func(**kwargs)

            ctx_logger.info(f"Tool {func.__name__} completed successfully")
            return result

        except Exception as e:
            # Log the error with context
            error_category = classify_exception(e)

            # Get session and phase info if available
            tool_context = kwargs.get('tool_context')
            session_id = tool_context.state.get("_session_id", "unknown") if tool_context else "unknown"
            phase = tool_context.state.get("current_phase", "unknown") if tool_context else "unknown"

            logger.error(
                f"Error in tool {func.__name__}: {type(e).__name__}: {str(e)}",
                exc_info=True,
                extra={"error_category": error_category.name, "session_id": session_id, "phase": phase}
            )

            # Create user-friendly error message
            user_message = create_user_error_message(e)

            # Return error response
            return {
                "success": False,
                "error": user_message,
                "error_type": type(e).__name__,
                "error_details": str(e)
            }

    return wrapper

# --- Graceful Degradation Utilities ---

def with_graceful_degradation(
    fallback_value: Any,
    fallback_message: str = "Using fallback due to error",
    log_level: int = logging.WARNING
) -> Callable[[F], F]:
    """
    Decorator to provide graceful degradation for non-critical functions.

    Args:
        fallback_value: Value to return if the function fails
        fallback_message: Message to log when falling back
        log_level: Log level to use for the fallback message

    Returns:
        Decorated function
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Log the error
                logger.log(
                    log_level,
                    f"{fallback_message} in {func.__name__}: {type(e).__name__}: {str(e)}",
                    exc_info=True
                )

                # Return fallback value
                return fallback_value

        return wrapper

    return decorator

# Async version of with_graceful_degradation
def with_async_graceful_degradation(
    fallback_value: Any,
    fallback_message: str = "Using fallback due to error",
    log_level: int = logging.WARNING
) -> Callable[[AsyncF], AsyncF]:
    """
    Decorator to provide graceful degradation for non-critical async functions.

    Args:
        fallback_value: Value to return if the function fails
        fallback_message: Message to log when falling back
        log_level: Log level to use for the fallback message

    Returns:
        Decorated async function
    """
    def decorator(func: AsyncF) -> AsyncF:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                # Log the error
                logger.log(
                    log_level,
                    f"{fallback_message} in async {func.__name__}: {type(e).__name__}: {str(e)}",
                    exc_info=True
                )

                # Return fallback value
                return fallback_value

        return wrapper

    return decorator

# --- Error Response Utilities ---

def create_error_response(exception: Exception, include_details: bool = False) -> Dict[str, Any]:
    """
    Create a standardized error response dictionary.

    Args:
        exception: The exception to create a response for
        include_details: Whether to include technical details in the response

    Returns:
        Error response dictionary
    """
    # Create user-friendly message
    user_message = create_user_error_message(exception)

    # Create basic response
    response = {
        "success": False,
        "error": user_message
    }

    # Add technical details if requested
    if include_details:
        response.update({
            "error_type": type(exception).__name__,
            "error_details": str(exception),
            "error_category": classify_exception(exception).name
        })

    return response
