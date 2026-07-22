from __future__ import annotations

from pathlib import Path

from nexus.skills import SkillManager


class BaseAgent:

    def __init__(
        self,
        llm=None,
    ):

        self.llm = llm

        self.skills = SkillManager(
            llm=llm,
        )

        self.skills.load(
            Path(__file__).parent.parent
            / "skills"
            / "definitions"
        )

    def run_skill(
        self,
        name: str,
        **kwargs,
    ):

        return self.skills.execute(
            name,
            **kwargs,
        )
