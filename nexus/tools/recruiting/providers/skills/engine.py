from __future__ import annotations

from .models import SkillDefinition


class SkillEngine:

    def __init__(
        self,
        llm,
    ):

        self.llm = llm

    def execute(
        self,
        skill: SkillDefinition,
        **kwargs,
    ):

        if skill.implementation:

            raise NotImplementedError(
                "Python implementations will be handled by the manager."
            )

        prompt = skill.prompt

        for key, value in kwargs.items():

            prompt = prompt.replace(
                "{{" + key + "}}",
                str(value),
            )

        return self.llm.generate(
            prompt
        )
