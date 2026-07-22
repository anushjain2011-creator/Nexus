from __future__ import annotations

from collections import defaultdict

from .models import SkillDefinition


class SkillRegistry:

    def __init__(self):

        self._skills: dict[
            str,
            SkillDefinition,
        ] = {}

        self._aliases: dict[
            str,
            str,
        ] = {}

        self._categories = defaultdict(
            set
        )

        self._tags = defaultdict(
            set
        )

    def register(
        self,
        skill: SkillDefinition,
    ):

        self._skills[
            skill.name
        ] = skill

        self._categories[
            skill.category
        ].add(
            skill.name
        )

        for tag in skill.tags:

            self._tags[
                tag
            ].add(
                skill.name
            )

    def register_many(
        self,
        skills: list[
            SkillDefinition
        ],
    ):

        for skill in skills:

            self.register(
                skill
            )

    def alias(
        self,
        alias: str,
        skill_name: str,
    ):

        self._aliases[
            alias
        ] = skill_name

    def get(
        self,
        name: str,
    ):

        if name in self._aliases:

            name = self._aliases[
                name
            ]

        return self._skills.get(
            name
        )

    def remove(
        self,
        name: str,
    ):

        skill = self._skills.pop(
            name,
            None,
        )

        if skill is None:

            return

        self._categories[
            skill.category
        ].discard(
            name
        )

        for tag in skill.tags:

            self._tags[
                tag
            ].discard(
                name
            )

    def categories(
        self,
    ):

        return sorted(
            self._categories.keys()
        )

    def skills_in_category(
        self,
        category: str,
    ):

        return [

            self._skills[name]

            for name in self._categories.get(
                category,
                [],
            )

        ]

    def skills_with_tag(
        self,
        tag: str,
    ):

        return [

            self._skills[name]

            for name in self._tags.get(
                tag,
                [],
            )

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

            )

        ]

    def all(
        self,
    ):

        return list(
            self._skills.values()
        )

    def names(
        self,
    ):

        return sorted(
            self._skills.keys()
        )

    def clear(
        self,
    ):

        self._skills.clear()

        self._aliases.clear()

        self._categories.clear()

        self._tags.clear()

    def __contains__(
        self,
        name: str,
    ):

        return name in self._skills

    def __len__(
        self,
    ):

        return len(
            self._skills
        )

    def __iter__(
        self,
    ):

        return iter(
            self._skills.values()
        )


skill_registry = SkillRegistry()
