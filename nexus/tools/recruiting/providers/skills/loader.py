from __future__ import annotations

from pathlib import Path

import yaml

from .models import SkillDefinition


class SkillLoader:

    def __init__(self):

        self._skills: dict[
            str,
            SkillDefinition,
        ] = {}

    @property
    def skills(self):

        return self._skills

    def load(
        self,
        directory: str | Path,
    ):

        directory = Path(directory)

        if not directory.exists():

            raise FileNotFoundError(
                directory
            )

        for file in directory.rglob(
            "*.yaml"
        ):

            self.load_file(file)

        return self._skills

    def load_file(
        self,
        file: str | Path,
    ):

        file = Path(file)

        with file.open(
            "r",
            encoding="utf-8",
        ) as f:

            data = yaml.safe_load(f) or {}

        category = file.stem

        for name, config in data.items():

            skill = SkillDefinition(

                name=f"{category}.{name}",

                description=config.get(
                    "description",
                    "",
                ),

                prompt=config.get(
                    "prompt",
                ),

                implementation=config.get(
                    "implementation",
                ),

                version=config.get(
                    "version",
                    "1.0.0",
                ),

                author=config.get(
                    "author",
                    "Nexus",
                ),

                category=config.get(
                    "category",
                    category,
                ),

                tags=config.get(
                    "tags",
                    [],
                ),

                inputs=config.get(
                    "inputs",
                    [],
                ),

                outputs=config.get(
                    "outputs",
                    [],
                ),

                permissions=config.get(
                    "permissions",
                    [],
                ),

                metadata=config.get(
                    "metadata",
                    {},
                ),

                enabled=config.get(
                    "enabled",
                    True,
                ),
            )

            self._skills[
                skill.name
            ] = skill

    def get(
        self,
        name: str,
    ):

        return self._skills.get(
            name
        )

    def remove(
        self,
        name: str,
    ):

        self._skills.pop(
            name,
            None,
        )

    def clear(self):

        self._skills.clear()

    def categories(self):

        return sorted(

            {

                skill.category

                for skill in self._skills.values()

            }

        )

    def by_category(
        self,
        category: str,
    ):

        return [

            skill

            for skill in self._skills.values()

            if skill.category == category

        ]

    def search(
        self,
        text: str,
    ):

        text = text.lower()

        return [

            skill

            for skill in self._skills.values()

            if (

                text in skill.name.lower()

                or text in skill.description.lower()

                or any(

                    text in tag.lower()

                    for tag in skill.tags

                )

            )

        ]

    def __len__(self):

        return len(
            self._skills
        )

    def __iter__(self):

        return iter(
            self._skills.values()
        )
