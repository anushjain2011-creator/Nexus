from __future__ import annotations

from .base import Skill


class SkillValidator:

    def validate(
        self,
        skill: Skill,
    ):

        if not skill.name:

            raise ValueError(
                "Skill requires a name."
            )

        if not callable(
            skill.execute
        ):

            raise ValueError(
                "Invalid execute method."
            )

        return True
