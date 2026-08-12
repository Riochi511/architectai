import json

from app.llm.gateway import LLMGateway
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

    gateway = LLMGateway()

    content = gateway.generate(
        system_prompt=EXTRACTOR_PROMPT,
        user_prompt=prompt,
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    requirements = json.loads(content)

    defaults = {
        "business_requirements": [],
        "functional_requirements": [],
        "non_functional_requirements": [],
        "business_rules": [],
        "user_stories": [],
        "acceptance_criteria": [],
        "use_cases": [],
        "assumptions": [],
        "risks": [],
        "open_questions": [],
    }

    for key, value in defaults.items():
        requirements.setdefault(key, value)

    return requirements