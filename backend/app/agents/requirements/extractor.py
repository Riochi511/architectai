import json

from litellm import completion

from app.config import settings
from app.agents.requirements.prompts import EXTRACTOR_PROMPT


def extract(discovery_memory: dict) -> dict:
    """
    Converts Discovery Memory into structured software requirements.

    Input:
        discovery_memory (dict)

    Output:
        {
            "business_requirements": [],
            "functional_requirements": [],
            "non_functional_requirements": [],
            "business_rules": [],
            "user_stories": [],
            "acceptance_criteria": [],
            "use_cases": [],
            "assumptions": [],
            "constraints": [],
            "risks": [],
            "open_questions": []
        }
    """

    prompt = f"""
Discovery Memory:

{json.dumps(discovery_memory, indent=2)}

Generate the complete structured requirements JSON.
"""

    response = completion(
        model=settings.MODEL_NAME,
        api_key=settings.OPENROUTER_API_KEY,
        api_base="https://openrouter.ai/api/v1",
        messages=[
            {
                "role": "system",
                "content": EXTRACTOR_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        response_format={
            "type": "json_object"
        },
    )

    content = response["choices"][0]["message"]["content"]

    requirements = json.loads(content)

    # Ensure every expected section exists.
    defaults = {
        "business_requirements": [],
        "functional_requirements": [],
        "non_functional_requirements": [],
        "business_rules": [],
        "user_stories": [],
        "acceptance_criteria": [],
        "use_cases": [],
        "assumptions": [],
        "constraints": [],
        "risks": [],
        "open_questions": [],
    }

    for key, value in defaults.items():
        requirements.setdefault(key, value)

    return requirements