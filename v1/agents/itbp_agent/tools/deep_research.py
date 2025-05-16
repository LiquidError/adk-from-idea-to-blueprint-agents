"""
Deep Research Tool Module

This module provides a comprehensive research tool that integrates with the Tavily Search API
to conduct in-depth research on product development topics. The tool is designed to:

1. Execute detailed searches on specific product development topics
2. Format research results in a structured, readable format
3. Handle errors gracefully with appropriate error messages
4. Provide both summary and detailed findings

The tool is used primarily by the Search Agent to support the Analyst Agent's
research needs during the brainstorming and research phases.
"""

import os
from typing import Dict, Any
import base64
import json
import asyncio

# Google Generative AI imports
from google.genai import types

# Pydantic for data validation
from pydantic import BaseModel, Field

# LangChain integrations
from langchain_tavily import TavilySearch as LangchainTavilySearch
from langchain_google_genai import ChatGoogleGenerativeAI

# ADK Tool imports
from google.adk.tools import ToolContext, FunctionTool

# Import logging and error handling
from ..shared_libraries.logging_config import get_logger, log_async_function_call, LogLevel
from ..shared_libraries.error_handling import (
    async_retry_on_error,
    RetryPolicy,
    ExternalServiceError,
    ValidationError,
    RateLimitError,
    ConfigurationError,
    NetworkError
)
from ..shared_libraries.error_middleware import handle_tool_errors

# Configure logger
logger = get_logger(__name__)

# --- Environment Variable Validation ---
REQUIRED_ENV_VARS = ["TAVILY_API_KEY", "GOOGLE_API_KEY"]

def _validate_env_vars() -> None:
    """
    Validate that all required environment variables are set.

    Raises:
        ConfigurationError: If any required environment variables are missing.
    """
    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var, None)]
    if missing_vars:
        # Log the error and raise an exception
        error_msg = f"Missing required environment variables for deep_research_tool: {', '.join(missing_vars)}"
        logger.error(error_msg)
        raise ConfigurationError(error_msg)

    logger.debug("Environment variable validation completed successfully.")

# Validate environment variables on module load
try:
    _validate_env_vars()
except ConfigurationError as e:
    logger.error(f"Environment validation failed: {str(e)}")
    # We'll let the tool function handle the error when it's called

# --- Simple Cache Implementation ---
class SearchCache:
    """
    Simple in-memory cache for search results to avoid redundant API calls.

    Attributes:
        _cache (Dict[str, Dict[str, Any]]): Dictionary mapping search queries to results.
        _max_size (int): Maximum number of entries in the cache.
        _ttl_seconds (int): Time-to-live for cache entries in seconds.
    """

    def __init__(self, max_size: int = 100, ttl_seconds: int = 3600):
        """
        Initialize the search cache.

        Args:
            max_size: Maximum number of entries in the cache.
            ttl_seconds: Time-to-live for cache entries in seconds.
        """
        self._cache = {}
        self._timestamps = {}
        self._max_size = max_size
        self._ttl_seconds = ttl_seconds
        logger.debug(f"Initialized SearchCache with max_size={max_size}, ttl_seconds={ttl_seconds}")

    async def get(self, key: str) -> Dict[str, Any]:
        """
        Get a result from the cache if it exists and is not expired.

        Args:
            key: The cache key (search query).

        Returns:
            The cached result or None if not found or expired.
        """
        import time

        if key not in self._cache:
            return None

        # Check if the entry has expired
        timestamp = self._timestamps.get(key, 0)
        if time.time() - timestamp > self._ttl_seconds:
            # Remove expired entry
            logger.debug(f"Cache entry expired for key: {key}")
            del self._cache[key]
            del self._timestamps[key]
            return None

        logger.debug(f"Cache hit for key: {key}")
        return self._cache[key]

    async def set(self, key: str, value: Dict[str, Any]) -> None:
        """
        Add a result to the cache.

        Args:
            key: The cache key (search query).
            value: The result to cache.
        """
        import time

        # If cache is full, remove the oldest entry
        if len(self._cache) >= self._max_size:
            oldest_key = min(self._timestamps, key=self._timestamps.get)
            del self._cache[oldest_key]
            del self._timestamps[oldest_key]
            logger.debug(f"Cache full, removed oldest entry: {oldest_key}")

        self._cache[key] = value
        self._timestamps[key] = time.time()
        logger.debug(f"Added to cache: {key}")

# Initialize the cache
search_cache = SearchCache()

# --- Tavily Search Result Models (Adapted from original) ---
class SearchResult(BaseModel):
    """
    Model for a single Product Development search result.

    Attributes:
        title: The title of the search result.
        url: The URL of the search result.
        content: The content snippet of the search result.
        score: The relevance score of the search result.
    """
    title: str = Field(..., description="The title of the search result")
    url: str = Field(..., description="The URL of the search result")
    content: str = Field(..., description="The content snippet of the search result")
    score: float = Field(..., description="The relevance score of the search result")

# --- Research Tool Implementation ---

@handle_tool_errors
@log_async_function_call(level=LogLevel.INFO)
@async_retry_on_error(max_retries=2, retry_policy=RetryPolicy.EXPONENTIAL_BACKOFF,
                     retry_exceptions=(ExternalServiceError, ConnectionError, TimeoutError))
async def _deep_research_tool_func(topic: str) -> Dict[str, str]:
    """
    Internal function for researching Product Development trends using Tavily search.

    This function performs a search on the specified topic using the Tavily Search API,
    formats the results, and returns them in a structured format. It includes caching
    to avoid redundant API calls and comprehensive error handling.

    Args:
        topic: The specific Product Development topic to research
              (e.g., 'technical difficulties with implementing this workflow and tech stack').

    Returns:
        A dictionary containing:
        - 'result' key with research findings if successful
        - 'error' key with error message if an error occurred
    """
    if not topic or not isinstance(topic, str) or len(topic.strip()) == 0:
        logger.error("Invalid topic provided: empty or not a string")
        raise ValidationError("Please provide a valid research topic as a non-empty string.")

    # Normalize the topic for caching (lowercase, trim whitespace)
    normalized_topic = topic.lower().strip()
    logger.info(f"Executing Product Development research tool for topic: '{normalized_topic}'")

    # Check cache first
    cached_result = await search_cache.get(normalized_topic)
    if cached_result:
        logger.info(f"Returning cached result for topic: '{normalized_topic}'")
        return cached_result

    # Validate environment variables before proceeding
    try:
        _validate_env_vars()
    except ConfigurationError as e:
        # Just re-raise the ConfigurationError
        raise e

    # Formulate a more specific search query for better results
    search_query = f"Current Product Development design trends and best practices for {normalized_topic}"
    logger.debug(f"Using Tavily search query: '{search_query}'")

    # Initialize Tavily Client with optimal parameters
    tavily_client = LangchainTavilySearch(
        max_results=5,
        search_depth="advanced",
        include_answer=True,  # Get a summarized answer
        include_raw_content=False,
        tavily_api_key=os.getenv("TAVILY_API_KEY")
    )

    try:
        # Execute the search asynchronously
        response = await asyncio.to_thread(
            tavily_client.invoke,
            {"query": search_query}
        )

        # Process the response
        results = [
            SearchResult(
                title=result["title"],
                url=result["url"],
                content=result["content"],
                score=result["score"]
            )
            for result in response.get("results", [])
        ]

        summary = response.get("answer", "No summary available from search.")

        # Check if we got meaningful results
        if not results and summary == "No summary available from search.":
            logger.warning(f"No results or summary found for topic: {normalized_topic}")
            result_dict = {"result": f"Could not find significant Product Development trends for: {normalized_topic}. Please try a more specific or different topic."}
            await search_cache.set(normalized_topic, result_dict)
            return result_dict

        # Format the output string with improved structure
        output = f"# Product Development Research Findings: {normalized_topic}\n\n"
        output += f"## Summary\n{summary}\n\n"

        if results:
            output += "## Top Results\n\n"
            for i, res in enumerate(results[:5], 1):  # Show top 5 results
                # Format content for better readability
                content_preview = res.content[:200] + ("..." if len(res.content) > 200 else "")
                output += f"### {i}. {res.title}\n"
                output += f"**Source**: [{res.url}]({res.url})\n\n"
                output += f"{content_preview}\n\n"

        logger.info(f"Research tool completed successfully for topic: '{normalized_topic}'")
        result_dict = {"result": output.strip()}

        # Cache the successful result
        await search_cache.set(normalized_topic, result_dict)
        return result_dict

    except ConnectionError as e:
        error_msg = f"Connection error during research: {str(e)}"
        logger.error(error_msg)
        raise NetworkError(error_msg)

    except TimeoutError as e:
        error_msg = f"Timeout error during research: {str(e)}"
        logger.error(error_msg)
        raise NetworkError(error_msg)

    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__

        # Classify the error
        if "API key" in error_msg:
            logger.error(f"API key error: {error_msg}")
            raise ConfigurationError("There was an issue with the API key. Please check your configuration.")
        elif "rate limit" in error_msg.lower():
            logger.error(f"Rate limit error: {error_msg}")
            raise RateLimitError("The search service rate limit has been reached. Please try again later.")
        else:
            logger.error(f"Unexpected error during research: {error_type}: {error_msg}", exc_info=True)
            raise ExternalServiceError(f"Error during research: {error_type}. Please try again with a different search query or check the service status.")

# Explicitly wrap the function using FunctionTool
# Update the docstring of the function to include the description
_deep_research_tool_func.__doc__ = """
Internal function for researching Product Development trends using Tavily search.

This function performs a search on the specified topic using the Tavily Search API,
formats the results, and returns them in a structured format. It includes caching
to avoid redundant API calls and comprehensive error handling.

Conducts comprehensive research on product development topics using the Tavily Search API.
This tool performs a deep search on the specified topic, providing both a summary and
detailed findings from multiple sources. It's designed to support market research,
competitive analysis, and trend identification for product development.

Args:
    topic: The specific product development topic to research
          (e.g., 'microservices architecture', 'AI-driven UX design', 'mobile app monetization strategies').

Returns:
    A dictionary containing:
    - 'result' key with research findings if successful
    - 'error' key with error message if an error occurred
"""

# Create the tool without the description parameter
deep_research_tool = FunctionTool(
    func=_deep_research_tool_func
    # The description will be derived from the function's docstring
)


