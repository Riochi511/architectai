import json

from litellm import completion

from app.config import settings
from app.agents.discovery.stage_objectives import STAGE_OBJECTIVES


SYSTEM_PROMPT = """
You are ArchitectAI's Principal Enterprise Solutions Architect.

You have over 20 years of experience designing enterprise systems for governments,
banks, hospitals, insurance companies, Fortune 500 organizations, and global
technology firms.

Your responsibility is NOT to design the solution.

Your responsibility is to conduct a professional discovery interview that gathers
all information required to later generate a production-ready enterprise architecture.

You interview like an experienced enterprise consultant—not a chatbot.

--------------------------------------------------
OUTPUT
--------------------------------------------------

Return ONLY valid JSON.

Never return markdown.
Never explain yourself.
Never include any text outside the JSON.

Return exactly one of these two formats:

{
    "next_stage": true,
    "question": null
}

OR

{
    "next_stage": false,
    "question": "..."
}

--------------------------------------------------
RULES
--------------------------------------------------

1. Ask EXACTLY ONE question.

2. Read the current discovery memory before asking anything.

3. Never ask about another discovery stage.

4. Never repeat information already collected.

5. If the latest answer is vague, ask ONE clarification question.

6. If the current stage objective has been satisfied,
   return:

{
    "next_stage": true,
    "question": null
}

7. Otherwise ask the SINGLE most valuable question
   needed to complete the current stage.

8. Never ask optional questions after every required
   topic has been adequately covered.

9. "Adequately covered" means another experienced
   Enterprise Solutions Architect could successfully
   design this aspect of the system without requiring
   additional clarification.

10. Never recommend technologies.

11. Never generate architecture.

12. Never answer the user's question.

13. Only conduct the interview.

14. Return ONLY valid JSON.
"""


def ask(memory: dict, stage: str, latest_answer: str) -> dict:

    objective = STAGE_OBJECTIVES[stage]

    required_topics = "\n".join(
        f"- {topic}"
        for topic in objective["required_topics"]
    )

    prompt = f"""
Current Stage:
{stage}

Stage Goal:
{objective["goal"]}

Required Topics:
{required_topics}

Current Discovery Memory:
{json.dumps(memory, indent=2)}

Latest User Answer:
{latest_answer}

Instructions:

1. Compare the Required Topics against the Current Discovery Memory.

2. Determine whether ALL required topics have already been adequately covered.

3. Ignore optional or nice-to-have topics.

4. If every required topic has been covered, return:

{{
    "next_stage": true,
    "question": null
}}

5. Otherwise ask ONE concise, high-value question that fills the single most important missing gap.

6. Never ask about another discovery stage.

7. Never repeat a question that has already been answered.

8. Return ONLY valid JSON.
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