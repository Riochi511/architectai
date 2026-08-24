from __future__ import annotations

import traceback
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
            "timeout": 180,
            "num_retries": 2,
        }

        if response_format is not None:
            request["response_format"] = response_format

        print()
        print("=" * 80)
        print("LLM GATEWAY: Sending request")
        print("=" * 80)
        print(
            f"Model: {settings.MODEL_NAME}"
        )
        print(
            "Provider: OpenRouter"
        )
        print(
            "API Base: https://openrouter.ai/api/v1"
        )
        print(
            f"Temperature: {temperature}"
        )
        print(
            f"Response Format: {response_format}"
        )
        print("=" * 80)

        try:

            response = completion(
                **request
            )

        except Exception as exc:

            print()
            print("=" * 80)
            print("LLM GATEWAY: REQUEST FAILED")
            print("=" * 80)

            print(
                f"Exception Type: "
                f"{type(exc).__name__}"
            )

            print(
                f"Exception: "
                f"{exc}"
            )

            print()
            print("FULL TRACEBACK")
            print("-" * 80)

            traceback.print_exc()

            print("=" * 80)
            print()

            raise

        print()
        print("=" * 80)
        print("LLM GATEWAY: Response received")
        print("=" * 80)

        try:
            content = (
                response["choices"][0]
                ["message"]
                ["content"]
            )

        except (
            KeyError,
            IndexError,
            TypeError,
        ) as exc:

            print(
                "LLM GATEWAY: Unexpected response "
                "structure."
            )

            print(
                f"Response: {response}"
            )

            raise RuntimeError(
                "LLM provider returned an "
                "unexpected response structure."
            ) from exc

        if not content:

            raise RuntimeError(
                "LLM provider returned an empty response."
            )

        print(
            f"Response length: {len(content)} characters"
        )

        print("=" * 80)
        print()

        return content.strip()