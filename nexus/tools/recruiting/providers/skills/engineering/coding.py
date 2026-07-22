from __future__ import annotations

from nexus.skills.base import Skill
from nexus.skills.registry import skill_registry


class CodingSkill(Skill):

    name = "engineering.coding"

    description = (
        "Generate, modify, and explain source code."
    )

    def execute(
        self,
        prompt: str,
        llm=None,
        **kwargs,
    ):

        if llm is None:
            raise ValueError(
                "An LLM instance is required."
            )

        return llm.generate(prompt)


skill_registry.register(
    CodingSkill()
)
