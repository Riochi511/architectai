import json
import traceback
from litellm import completion

from app.config import settings


class ArchitectureEngine:

    def generate(
        self,
        system_prompt: str,
        section_prompt: str,
        project_context: dict,
    ) -> str:

        prompt = f"""
Project Context

{json.dumps(project_context, indent=2)}

Task

{section_prompt}
"""

        try:
            response = completion(
                model=settings.MODEL_NAME,
                api_key=settings.OPENROUTER_API_KEY,
                api_base="https://openrouter.ai/api/v1",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.2,
            )

            return response["choices"][0]["message"]["content"].strip()

        except Exception as e:
            import traceback

            print("=" * 80)
            print("EXCEPTION TYPE:", type(e).__name__)
            print("EXCEPTION:", e)
            traceback.print_exc()
            print("=" * 80)

            raise