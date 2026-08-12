import json

from app.llm.gateway import LLMGateway


SYSTEM_PROMPT = """
You are an Enterprise Business Analyst.

Your ONLY responsibility is maintaining the project's discovery memory.

You receive:

- the current discovery stage
- the existing discovery memory
- the latest user answer

Your task is to improve the memory.

Rules:

- Update ONLY the section related to the current stage.
- Preserve all previously collected information.
- Never remove useful information.
- Merge duplicate information.
- Rewrite the updated section using concise, professional business language.
- Return the COMPLETE discovery memory object.
- Return ONLY valid JSON.
- Never include markdown.
- Never include explanations.
"""


def refine(
    memory: dict,
    stage: str,
    latest_answer: str,
) -> dict:

    prompt = f"""
Current Stage:
{stage}

Current Discovery Memory:
{json.dumps(memory, indent=2)}

Latest User Answer:
{latest_answer}
"""

    gateway = LLMGateway()

    content = gateway.generate(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    return json.loads(content)