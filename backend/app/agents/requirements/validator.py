import json

from app.llm.gateway import LLMGateway
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

    gateway = LLMGateway()

    content = gateway.generate(
        system_prompt=VALIDATOR_PROMPT,
        user_prompt=prompt,
        temperature=0.1,
        response_format={"type": "json_object"},
    )

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