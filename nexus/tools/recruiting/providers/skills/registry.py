from __future__ import annotations

from .base import Skill


class SkillRegistry:

    def __init__(self):

        self._skills = {}

    def register(
        self,
        skill: Skill,
    ):

        self._skills[
            skill.name
        ] = skill

    def unregister(
        self,
        name: str,
    ):

        self._skills.pop(
            name,
            None,
        )

    def get(
        self,
        name: str,
    ):

        return self._skills.get(
            name
        )

    def all(self):

        return list(
            self._skills.values()
        )


skill_registry = SkillRegistry()
