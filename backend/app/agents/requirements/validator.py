import json

from litellm import completion

from app.config import settings
from app.agents.requirements.prompts import VALIDATOR_PROMPT


def validate(requirements: dict) -> dict:
    """
    Validates extracted requirements.

    Input:
        requirements (dict)

    Output:
        {
            "valid": bool,
            "issues": [],
            "warnings": [],
            "missing_sections": []
        }
    """

    prompt = f"""
Requirements:

{json.dumps(requirements, indent=2)}

Review these requirements and produce the validation report.
"""

    response = completion(
        model=settings.MODEL_NAME,
        api_key=settings.OPENROUTER_API_KEY,
        api_base="https://openrouter.ai/api/v1",
        messages=[
            {
                "role": "system",
                "content": VALIDATOR_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.1,
        response_format={
            "type": "json_object"
        },
    )

    content = response["choices"][0]["message"]["content"]

    report = json.loads(content)

    defaults = {
        "valid": True,
        "issues": [],
        "warnings": [],
        "missing_sections": [],
    }

    for key, value in defaults.items():
        report.setdefault(key, value)

    # ----------------------------------------
    # Determine validity from actual issues
    # ----------------------------------------

    report["valid"] = len(
        report.get("issues", [])
    ) == 0

    return report