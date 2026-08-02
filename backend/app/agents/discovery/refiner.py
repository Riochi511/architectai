import json

from litellm import completion

from app.config import settings


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

    response = completion(
        model=settings.MODEL_NAME,
        api_key=settings.OPENROUTER_API_KEY,
        api_base="https://openrouter.ai/api/v1",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    content = response["choices"][0]["message"]["content"]

    return json.loads(content)