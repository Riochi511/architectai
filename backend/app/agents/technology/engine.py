from __future__ import annotations

import json
import traceback

from app.llm.gateway import LLMGateway


class TechnologyEngine:
    """
    Technology decision generation engine.

    The engine is provider-agnostic.
    All LLM communication is handled by the central
    LLM Gateway.
    """

    def __init__(self):
        self.llm = LLMGateway()

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
            return self.llm.generate(
                system_prompt=system_prompt,
                user_prompt=prompt,
                temperature=0.2,
            )

        except Exception as e:
            print("=" * 80)
            print("EXCEPTION TYPE:", type(e).__name__)
            print("EXCEPTION:", e)
            traceback.print_exc()
            print("=" * 80)

            raise