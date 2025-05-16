"""
Error Handling Module

This module provides a comprehensive error handling framework for the Idea-to-Blueprint-Pipeline project.
It includes:

1. Custom exception classes for different error types
2. Error classification and categorization
3. Retry mechanisms for transient errors
4. Error handling decorators for functions and methods
5. User-friendly error message generation
"""

import logging
import time
import functools
import traceback
import asyncio
from enum import Enum, auto
from typing import Dict, Any, Optional, Callable, TypeVar, Union, List, Tuple, Type

from .logging_config import ErrorCategory, RetryPolicy, get_logger

# Get module logger
logger = get_logger(__name__)

# --- Custom Exception Classes ---

class ITBPMethodError(Exception):
    """Base exception class for all Idea-to-Blueprint-Pipeline errors."""

    def __init__(self, message: str, error_category: ErrorCategory = ErrorCategory.UNKNOWN,
                 retry_policy: RetryPolicy = RetryPolicy.NO_RETRY,
                 user_message: Optional[str] = None):
        """
        Initialize the exception.

        Args:
            message: Technical error message
            error_category: Category of the error
            retry_policy: Retry policy for this error
            user_message: User-friendly error message (if None, a generic message will be used)
        """
        self.error_category = error_category
        self.retry_policy = retry_policy
        self.user_message = user_message or self._get_default_user_message(message, error_category)
        super().__init__(message)

    def _get_default_user_message(self, message: str, category: ErrorCategory) -> str:
        """Generate a default user-friendly message based on the error category."""
        base_msg = "An error occurred"

        category_messages = {
            ErrorCategory.CONFIGURATION: "A configuration error occurred. Please check your settings.",
            ErrorCategory.NETWORK: "A network error occurred. Please check your connection and try again.",
            ErrorCategory.STATE: "A state management error occurred. Your session may need to be restarted.",
            ErrorCategory.VALIDATION: "A validation error occurred. Please check your inputs.",
            ErrorCategory.EXTERNAL_SERVICE: "An external service error occurred. The service may be unavailable.",
            ErrorCategory.INTERNAL: "An internal error occurred. Please try again later.",
            ErrorCategory.SECURITY: "A security error occurred. Please check your credentials.",
            ErrorCategory.USER_INPUT: "An input error occurred. Please check your input and try again.",
            ErrorCategory.RESOURCE: "A resource error occurred. The requested resource may not be available.",
            ErrorCategory.UNKNOWN: "An unexpected error occurred. Please try again later."
        }

        return category_messages.get(category, base_msg)

# Configuration errors
class ConfigurationError(ITBPMethodError):
    """Error raised when there's a configuration issue."""

    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(
            message,
            error_category=ErrorCategory.CONFIGURATION,
            retry_policy=RetryPolicy.NO_RETRY,
            user_message=user_message
        )

# Network errors
class NetworkError(ITBPMethodError):
    """Error raised when there's a network issue."""

    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(
            message,
            error_category=ErrorCategory.NETWORK,
            retry_policy=RetryPolicy.EXPONENTIAL_BACKOFF,
            user_message=user_message
        )

# State management errors
class StateError(ITBPMethodError):
    """Error raised when there's a state management issue."""

    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(
            message,
            error_category=ErrorCategory.STATE,
            retry_policy=RetryPolicy.NO_RETRY,
            user_message=user_message
        )

# Validation errors
class ValidationError(ITBPMethodError):
    """Error raised when there's a validation issue."""

    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(
            message,
            error_category=ErrorCategory.VALIDATION,
            retry_policy=RetryPolicy.NO_RETRY,
            user_message=user_message
        )

# External service errors
class ExternalServiceError(ITBPMethodError):
    """Error raised when there's an issue with an external service."""

    def __init__(self, message: str, user_message: Optional[str] = None,
                 retry_policy: RetryPolicy = RetryPolicy.EXPONENTIAL_BACKOFF):
        super().__init__(
            message,
            error_category=ErrorCategory.EXTERNAL_SERVICE,
            retry_policy=retry_policy,
            user_message=user_message
        )

# Rate limit errors (special case of external service errors)
class RateLimitError(ExternalServiceError):
    """Error raised when an external service rate limit is reached."""

    def __init__(self, message: str, user_message: Optional[str] = None):
        user_msg = user_message or "Rate limit reached. Please try again later."
        super().__init__(
            message,
            user_message=user_msg,
            retry_policy=RetryPolicy.EXPONENTIAL_BACKOFF
        )

# --- Error Handling Utilities ---

# Function type for type hints
F = TypeVar('F', bound=Callable[..., Any])

def retry_on_error(
    max_retries: int = 3,
    retry_exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
    retry_policy: RetryPolicy = RetryPolicy.EXPONENTIAL_BACKOFF,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    logger: Optional[logging.Logger] = None
) -> Callable[[F], F]:
    """
    Decorator to retry a function on specific exceptions.

    Args:
        max_retries: Maximum number of retry attempts
        retry_exceptions: Exception types to retry on
        retry_policy: Retry policy to use
        base_delay: Base delay in seconds for backoff
        max_delay: Maximum delay in seconds
        logger: Logger to use (if None, a logger will be created based on the module name)

    Returns:
        Decorated function
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get or create logger
            nonlocal logger
            if logger is None:
                logger = logging.getLogger(func.__module__)

            attempt = 0
            last_exception = None

            while attempt <= max_retries:
                try:
                    if attempt > 0:
                        logger.info(f"Retry attempt {attempt}/{max_retries} for {func.__name__}")

                    return func(*args, **kwargs)

                except retry_exceptions as e:
                    attempt += 1
                    last_exception = e

                    # Check if we've reached max retries
                    if attempt > max_retries:
                        logger.error(f"Max retries ({max_retries}) exceeded for {func.__name__}: {str(e)}")
                        break

                    # Calculate delay based on retry policy
                    if retry_policy == RetryPolicy.NO_RETRY:
                        break
                    elif retry_policy == RetryPolicy.IMMEDIATE:
                        delay = 0
                    elif retry_policy == RetryPolicy.EXPONENTIAL_BACKOFF:
                        delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                    elif retry_policy == RetryPolicy.LINEAR_BACKOFF:
                        delay = min(base_delay * attempt, max_delay)
                    elif retry_policy == RetryPolicy.CONSTANT_DELAY:
                        delay = base_delay
                    else:
                        delay = 0

                    # Log the retry
                    logger.warning(
                        f"Error in {func.__name__} (attempt {attempt}/{max_retries}), "
                        f"retrying in {delay:.2f}s: {type(e).__name__}: {str(e)}"
                    )

                    # Wait before retrying
                    time.sleep(delay)

            # If we get here, all retries failed
            if last_exception:
                raise last_exception

        return wrapper

    return decorator

# Async version of retry_on_error
def async_retry_on_error(
    max_retries: int = 3,
    retry_exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
    retry_policy: RetryPolicy = RetryPolicy.EXPONENTIAL_BACKOFF,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    logger: Optional[logging.Logger] = None
) -> Callable[[F], F]:
    """
    Decorator to retry an async function on specific exceptions.

    Args:
        max_retries: Maximum number of retry attempts
        retry_exceptions: Exception types to retry on
        retry_policy: Retry policy to use
        base_delay: Base delay in seconds for backoff
        max_delay: Maximum delay in seconds
        logger: Logger to use (if None, a logger will be created based on the module name)

    Returns:
        Decorated async function
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Get or create logger
            nonlocal logger
            if logger is None:
                logger = logging.getLogger(func.__module__)

            attempt = 0
            last_exception = None

            while attempt <= max_retries:
                try:
                    if attempt > 0:
                        logger.info(f"Retry attempt {attempt}/{max_retries} for async {func.__name__}")

                    return await func(*args, **kwargs)

                except retry_exceptions as e:
                    attempt += 1
                    last_exception = e

                    # Check if we've reached max retries
                    if attempt > max_retries:
                        logger.error(f"Max retries ({max_retries}) exceeded for async {func.__name__}: {str(e)}")
                        break

                    # Calculate delay based on retry policy
                    if retry_policy == RetryPolicy.NO_RETRY:
                        break
                    elif retry_policy == RetryPolicy.IMMEDIATE:
                        delay = 0
                    elif retry_policy == RetryPolicy.EXPONENTIAL_BACKOFF:
                        delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                    elif retry_policy == RetryPolicy.LINEAR_BACKOFF:
                        delay = min(base_delay * attempt, max_delay)
                    elif retry_policy == RetryPolicy.CONSTANT_DELAY:
                        delay = base_delay
                    else:
                        delay = 0

                    # Log the retry
                    logger.warning(
                        f"Error in async {func.__name__} (attempt {attempt}/{max_retries}), "
                        f"retrying in {delay:.2f}s: {type(e).__name__}: {str(e)}"
                    )

                    # Wait before retrying
                    await asyncio.sleep(delay)

            # If we get here, all retries failed
            if last_exception:
                raise last_exception

        return wrapper

    return decorator

# Function to create a user-friendly error message
def create_user_error_message(exception: Exception) -> str:
    """
    Create a user-friendly error message from an exception.

    Args:
        exception: The exception to create a message for

    Returns:
        A user-friendly error message
    """
    if isinstance(exception, ITBPMethodError) and exception.user_message:
        return exception.user_message

    # Default messages based on exception type
    if isinstance(exception, (ConnectionError, TimeoutError)):
        return "A network error occurred. Please check your connection and try again."
    elif isinstance(exception, PermissionError):
        return "You don't have permission to perform this action."
    elif isinstance(exception, FileNotFoundError):
        return "The requested file could not be found."
    elif isinstance(exception, ValueError):
        return "Invalid input provided. Please check your input and try again."
    elif isinstance(exception, KeyError):
        return "A required value is missing. Please check your input and try again."
    elif isinstance(exception, TypeError):
        return "An unexpected type error occurred. Please check your input and try again."

    # Generic message for other exceptions
    return "An unexpected error occurred. Please try again later."

# Function to classify an exception
def classify_exception(exception: Exception) -> ErrorCategory:
    """
    Classify an exception into an error category.

    Args:
        exception: The exception to classify

    Returns:
        The error category
    """
    if isinstance(exception, ITBPMethodError):
        return exception.error_category

    # Classify based on exception type
    if isinstance(exception, (ConnectionError, TimeoutError)):
        return ErrorCategory.NETWORK
    elif isinstance(exception, (ValueError, TypeError, KeyError)):
        return ErrorCategory.VALIDATION
    elif isinstance(exception, (FileNotFoundError, PermissionError)):
        return ErrorCategory.RESOURCE
    elif isinstance(exception, (ImportError, ModuleNotFoundError)):
        return ErrorCategory.CONFIGURATION

    # Default to INTERNAL for unclassified exceptions
    return ErrorCategory.INTERNAL
