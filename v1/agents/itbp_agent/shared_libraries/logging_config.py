"""
Centralized Logging Configuration Module

This module provides a centralized configuration for logging across the entire
Idea-to-Blueprint-Pipeline project. It includes:

1. Structured logging with appropriate levels
2. Console and file handlers with different formats
3. Log rotation and management
4. Custom formatters for different output destinations
5. Error classification and handling utilities
"""

import logging
import logging.handlers
import os
import sys
import json
import traceback
import functools
import inspect
import time
from enum import Enum, auto
from typing import Dict, Any, Optional, Callable, TypeVar, Union, List, Tuple

# Define log directory
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Define log levels
class LogLevel(Enum):
    """Custom log levels for more granular control."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

# Define error categories for classification
class ErrorCategory(Enum):
    """Categories of errors for better error handling and reporting."""
    CONFIGURATION = auto()  # Configuration errors (missing env vars, invalid config)
    NETWORK = auto()        # Network-related errors (API calls, connectivity)
    STATE = auto()          # State management errors (invalid state, persistence failures)
    VALIDATION = auto()     # Validation errors (invalid inputs, schema violations)
    EXTERNAL_SERVICE = auto()  # External service errors (API failures, rate limits)
    INTERNAL = auto()       # Internal errors (unexpected exceptions, logic errors)
    SECURITY = auto()       # Security-related errors (auth failures, permission issues)
    USER_INPUT = auto()     # User input errors (invalid commands, format issues)
    RESOURCE = auto()       # Resource errors (file not found, permission denied)
    UNKNOWN = auto()        # Uncategorized errors

# Define retry policies for different error types
class RetryPolicy(Enum):
    """Retry policies for different types of operations."""
    NO_RETRY = auto()       # Do not retry
    IMMEDIATE = auto()      # Retry immediately
    EXPONENTIAL_BACKOFF = auto()  # Retry with exponential backoff
    LINEAR_BACKOFF = auto()  # Retry with linear backoff
    CONSTANT_DELAY = auto()  # Retry with constant delay

# Custom JSON formatter for structured logging
class JsonFormatter(logging.Formatter):
    """
    Custom formatter that outputs logs in JSON format for easier parsing.
    """
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if available
        if record.exc_info:
            log_record["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info)
            }
        
        # Add extra fields if available
        if hasattr(record, "error_category"):
            log_record["error_category"] = record.error_category
        
        if hasattr(record, "session_id"):
            log_record["session_id"] = record.session_id
            
        if hasattr(record, "phase"):
            log_record["phase"] = record.phase
            
        if hasattr(record, "duration_ms"):
            log_record["duration_ms"] = record.duration_ms
            
        # Add any other custom fields from record.__dict__
        for key, value in record.__dict__.items():
            if key not in ["args", "exc_info", "exc_text", "stack_info", "lineno", 
                          "funcName", "module", "msg", "name", "pathname", 
                          "process", "processName", "thread", "threadName",
                          "levelname", "levelno", "created", "msecs", 
                          "relativeCreated", "filename"]:
                try:
                    # Try to serialize the value to avoid JSON encoding errors
                    json.dumps({key: value})
                    log_record[key] = value
                except (TypeError, OverflowError):
                    # If the value can't be serialized, convert it to a string
                    log_record[key] = str(value)
        
        return json.dumps(log_record)

# Configure the root logger
def configure_logging(
    console_level: LogLevel = LogLevel.INFO,
    file_level: LogLevel = LogLevel.DEBUG,
    log_file: str = "ITBP_agent.log",
    max_bytes: int = 10485760,  # 10MB
    backup_count: int = 5,
    enable_json_logging: bool = False
) -> None:
    """
    Configure the logging system with console and file handlers.
    
    Args:
        console_level: Minimum log level for console output
        file_level: Minimum log level for file output
        log_file: Name of the log file
        max_bytes: Maximum size of each log file before rotation
        backup_count: Number of backup log files to keep
        enable_json_logging: Whether to use JSON formatting for log files
    """
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Capture all logs, handlers will filter
    
    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level.value)
    console_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    console_handler.setFormatter(logging.Formatter(console_format))
    root_logger.addHandler(console_handler)
    
    # Create file handler with rotation
    log_path = os.path.join(LOG_DIR, log_file)
    file_handler = logging.handlers.RotatingFileHandler(
        log_path, maxBytes=max_bytes, backupCount=backup_count
    )
    file_handler.setLevel(file_level.value)
    
    if enable_json_logging:
        file_handler.setFormatter(JsonFormatter())
    else:
        file_format = "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s"
        file_handler.setFormatter(logging.Formatter(file_format))
    
    root_logger.addHandler(file_handler)
    
    # Log the configuration
    root_logger.info(f"Logging configured: console={console_level.name}, file={file_level.name}, path={log_path}")

# Custom logger class with additional context
class ContextLogger(logging.LoggerAdapter):
    """
    Logger adapter that adds context information to log records.
    """
    def process(self, msg, kwargs):
        # Add extra context from the adapter to the record
        kwargs.setdefault("extra", {}).update(self.extra)
        return msg, kwargs
    
    def error_with_category(self, msg, error_category: ErrorCategory, *args, **kwargs):
        """Log an error with a specific category."""
        kwargs.setdefault("extra", {})["error_category"] = error_category.name
        self.error(msg, *args, **kwargs)

# Function to get a logger with context
def get_logger(name: str, session_id: Optional[str] = None, phase: Optional[str] = None) -> ContextLogger:
    """
    Get a logger with optional context information.
    
    Args:
        name: Logger name (usually __name__)
        session_id: Optional session ID for context
        phase: Optional workflow phase for context
        
    Returns:
        A ContextLogger instance with the specified context
    """
    logger = logging.getLogger(name)
    extra = {}
    
    if session_id:
        extra["session_id"] = session_id
    
    if phase:
        extra["phase"] = phase
    
    return ContextLogger(logger, extra)

# Function type for type hints
F = TypeVar('F', bound=Callable[..., Any])

# Decorator for logging function calls with timing
def log_function_call(logger: Optional[logging.Logger] = None, level: LogLevel = LogLevel.DEBUG) -> Callable[[F], F]:
    """
    Decorator to log function calls with timing information.
    
    Args:
        logger: Logger to use (if None, a logger will be created based on the module name)
        level: Log level to use
        
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
            
            # Log function call
            arg_str = ", ".join([repr(a) for a in args] + [f"{k}={repr(v)}" for k, v in kwargs.items()])
            logger.log(level.value, f"Calling {func.__name__}({arg_str})")
            
            # Call function and time it
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                logger.log(level.value, f"{func.__name__} completed in {duration_ms:.2f}ms")
                return result
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                logger.error(
                    f"{func.__name__} failed after {duration_ms:.2f}ms: {type(e).__name__}: {str(e)}",
                    exc_info=True
                )
                raise
        
        return wrapper
    
    return decorator

# Async version of the log_function_call decorator
def log_async_function_call(logger: Optional[logging.Logger] = None, level: LogLevel = LogLevel.DEBUG) -> Callable[[F], F]:
    """
    Decorator to log async function calls with timing information.
    
    Args:
        logger: Logger to use (if None, a logger will be created based on the module name)
        level: Log level to use
        
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
            
            # Log function call
            arg_str = ", ".join([repr(a) for a in args] + [f"{k}={repr(v)}" for k, v in kwargs.items()])
            logger.log(level.value, f"Calling async {func.__name__}({arg_str})")
            
            # Call function and time it
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                logger.log(level.value, f"Async {func.__name__} completed in {duration_ms:.2f}ms")
                return result
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                logger.error(
                    f"Async {func.__name__} failed after {duration_ms:.2f}ms: {type(e).__name__}: {str(e)}",
                    exc_info=True
                )
                raise
        
        return wrapper
    
    return decorator

# Initialize logging with default configuration
configure_logging()
