from __future__ import annotations

from pathlib import Path

from .engine import SkillEngine
from .loader import SkillLoader
from .registry import SkillRegistry


class SkillManager:

    def __init__(
        self,
        llm=None,
    ):

        self.loader = SkillLoader()

        self.registry = SkillRegistry()

        self.engine = SkillEngine(
            llm=llm,
        )

    def load(
        self,
        directory: str | Path,
    ):

        skills = self.loader.load(
            directory,
        )

        self.registry.clear()

        self.registry.register_many(
            list(
                skills.values()
            )
        )

    def execute(
        self,
        name: str,
        **kwargs,
    ):

        skill = self.registry.get(
            name,
        )

        if skill is None:

            raise ValueError(
                f"Unknown skill '{name}'."
            )

        return self.engine.execute(
            skill,
            **kwargs,
        )

    def get(
        self,
        name: str,
    ):

        return self.registry.get(
            name,
        )

    def all(self):

        return self.registry.all()

    def names(self):

        return self.registry.names()

    def categories(self):

        return self.registry.categories()

    def search(
        self,
        text: str,
    ):

        return self.registry.search(
            text,
        )

    def skills_in_category(
        self,
        category: str,
    ):

        return self.registry.skills_in_category(
            category,
        )

    def reload(
        self,
        directory: str | Path,
    ):

        self.load(
            directory,
        )


skill_manager = SkillManager()
