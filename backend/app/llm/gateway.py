from typing import Optional

from litellm import completion

from app.config import settings


class LLMGateway:
    """
    Central gateway for all LLM interactions in ArchitectAI.

    Agents communicate with the LLM exclusively through this gateway.

    The gateway is responsible for:
    - provider configuration
    - model selection
    - request formatting
    - structured response requests
    - timeout handling
    - transient provider retries

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

            # Give slower LLM responses enough time to complete.
            "timeout": 180,

            # Retry transient provider/network failures.
            "num_retries": 2,
        }

        if response_format is not None:
            request["response_format"] = response_format

        response = completion(**request)

        content = response["choices"][0]["message"]["content"]

        if not content:
            raise RuntimeError(
                "LLM provider returned an empty response."
            )

        return content.strip()