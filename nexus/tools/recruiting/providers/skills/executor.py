from __future__ import annotations

from .manager import skill_manager


class SkillExecutor:

    def run(
        self,
        skill: str,
        **kwargs,
    ):

        return skill_manager.execute(
            skill,
            **kwargs,
        )
