from __future__ import annotations

import json
import traceback

from app.llm.gateway import LLMGateway


class CriticEngine:
    """
    Cross-stage architecture and engineering critique engine.

    The engine is provider-agnostic.
    All LLM communication is handled by the central
    LLM Gateway.

    The Critic does not redesign the system.

    It evaluates whether the accumulated engineering
    artifacts are sufficiently consistent, traceable,
    defensible, and ready for Blueprint generation.
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

{json.dumps(
    project_context,
    indent=2,
)}


Task

{section_prompt}
"""

        try:
            return self.llm.generate(
                system_prompt=system_prompt,
                user_prompt=prompt,
                temperature=0.1,
            )

        except Exception as e:
            print("=" * 80)
            print("EXCEPTION TYPE:", type(e).__name__)
            print("EXCEPTION:", e)
            traceback.print_exc()
            print("=" * 80)

            raise
