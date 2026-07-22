from __future__ import annotations

from .registry import skill_registry


class SkillManager:

    def execute(
        self,
        name: str,
        **kwargs,
    ):

        skill = skill_registry.get(
            name
        )

        if skill is None:

            raise ValueError(
                f"Unknown skill '{name}'."
            )

        return skill.execute(
            **kwargs
        )

    def register(
        self,
        skill,
    ):

        skill_registry.register(
            skill
        )

    def skills(self):

        return skill_registry.all()


skill_manager = SkillManager()
