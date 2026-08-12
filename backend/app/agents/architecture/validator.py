import json

from app.llm.gateway import LLMGateway


VALIDATOR_SYSTEM_PROMPT = """
You are a Principal Enterprise Software Architect.

Your task is to review ONE completed Software Architecture Document.

Evaluate it for completeness and quality.

Return ONLY valid JSON.

Format:

{
    "valid": true,
    "confidence": 96,
    "issues": [],
    "warnings": [],
    "missing_sections": [],
    "recommendations": []
}

Validation Rules

Check whether the document contains:

- Executive Summary
- Business Context
- Functional Architecture
- Data Architecture
- API Architecture
- AI Architecture (if applicable)
- Security
- Deployment
- DevOps
- Technology Decisions
- Risks

Also evaluate:

- Internal consistency
- Technical completeness
- Enterprise quality
- Clarity
- Missing assumptions
- Missing architectural decisions

Never return markdown.

Never explain your reasoning.

Return JSON only.
"""


def validate(document: str) -> dict:
    """
    Validates a generated Software Architecture Document.
    """

    prompt = f"""
Architecture Document

{document}
"""

    gateway = LLMGateway()

    response = gateway.generate(
        system_prompt=VALIDATOR_SYSTEM_PROMPT,
        user_prompt=prompt,
        temperature=0.1,
        response_format={
            "type": "json_object"
        },
    )

    report = json.loads(response)

    defaults = {
        "valid": True,
        "confidence": 100,
        "issues": [],
        "warnings": [],
        "missing_sections": [],
        "recommendations": [],
    }

    for key, value in defaults.items():
        report.setdefault(key, value)

    return report