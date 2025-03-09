# ai_client.py
from openai import OpenAI
from app.core.config import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL
)
