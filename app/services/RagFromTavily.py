from tavily import TavilyClient
from app.core.config import settings
import asyncio
from typing import Dict, List, Any, Optional
from app.core.log_config import logger

async def search_tavily(query: str, max_results: int = 6) -> Dict[str, Any]:
    """
    Asynchronous function to search using Tavily API and format the results.

    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 6)

    Returns:
        Dict containing:
        - contents: Formatted string of all results' content
        - results: Original results from Tavily
    """

    # Create a function to run in a thread
    def run_search():
        tavily_client = TavilyClient(api_key=settings.TAVILY_SEARCH_API)
        return tavily_client.search(query=query, max_results=max_results)

    # Run the synchronous Tavily search in a thread pool to make it async
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, run_search)

    # Extract the results from the response
    results = response.get('results', [])

    # Format the contents as requested
    contents = ""
    for i, result in enumerate(results):
        contents += f"网页{i + 1}：{result.get('content', '')}\n\n"

    # Remove the last newlines if they exist
    contents = contents.rstrip()
    logger.info(f"互联网检索信息为:{results}")
    return {
        "contents": contents,
        "results": results
    }