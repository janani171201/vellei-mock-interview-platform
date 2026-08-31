import json
from app.config import settings

def call_llm(system: str, user: str):
    if not settings.openai_api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.responses.create(
            model=settings.openai_model,
            instructions=system,
            input=user
        )
        return json.loads(response.output_text)
    except Exception:
        return None
