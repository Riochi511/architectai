from typing import Optional

from litellm import completion

from app.config import settings


class LLMGateway:
    """
    Central gateway for all LLM interactions in ArchitectAI.

    Agents must communicate with the LLM through this gateway.
    Agents should never know which provider or model is being used.
    """

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        response_format: Optional[dict] = None,
    ) -> str:

        request = {
            "model": settings.MODEL_NAME,
            "api_key": settings.OPENROUTER_API_KEY,
            "api_base": "https://openrouter.ai/api/v1",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            "temperature": temperature,
        }

        if response_format is not None:
            request["response_format"] = response_format

        response = completion(**request)

        return response["choices"][0]["message"]["content"].strip()