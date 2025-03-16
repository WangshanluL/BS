from tavily import TavilyClient
from app.core.config import settings

tavily_client = TavilyClient(api_key=settings.TAVILY_SEARCH_API)
response = tavily_client.search(query="什么是抖动（thrashing），为什么会发生？如何避免？",max_results=6)

print(response)