import requests

from app.config import settings
from app.services.prompt_builder import build_architecture_prompt
from app.models.project import Project


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def generate_architecture(project: Project) -> str:
    """
    Generate a software architecture
    using OpenRouter.
    """

    prompt = build_architecture_prompt(project)

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert software architect. "
                    "Generate professional architecture documents."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.3,
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]