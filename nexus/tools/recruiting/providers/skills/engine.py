from __future__ import annotations

import importlib
import re

from .models import SkillDefinition, SkillResult


class SkillEngine:

    def __init__(
        self,
        llm=None,
    ):

        self.llm = llm

    def execute(
        self,
        skill: SkillDefinition,
        **kwargs,
    ) -> SkillResult:

        if not skill.enabled:

            return SkillResult(
                success=False,
                error=f"Skill '{skill.name}' is disabled.",
            )

        if skill.implementation:

            return self._execute_implementation(
                skill,
                **kwargs,
            )

        if skill.prompt:

            return self._execute_prompt(
                skill,
                **kwargs,
            )

        return SkillResult(
            success=False,
            error=f"Skill '{skill.name}' has no execution method.",
        )

    def _execute_prompt(
        self,
        skill: SkillDefinition,
        **kwargs,
    ) -> SkillResult:

        if self.llm is None:

            return SkillResult(
                success=False,
                error="No LLM configured.",
            )

        prompt = self._render_prompt(
            skill.prompt,
            kwargs,
        )

        response = self.llm.generate(
            prompt
        )

        return SkillResult(
            success=True,
            output=response,
            metadata={
                "skill": skill.name,
                "type": "prompt",
            },
        )

    def _execute_implementation(
        self,
        skill: SkillDefinition,
        **kwargs,
    ) -> SkillResult:

        module = importlib.import_module(
            f"nexus.skills.implementations.{skill.implementation}"
        )

        if not hasattr(
            module,
            "execute",
        ):

            return SkillResult(
                success=False,
                error=f"{skill.implementation} has no execute() function.",
            )

        output = module.execute(
            **kwargs,
        )

        return SkillResult(
            success=True,
            output=output,
            metadata={
                "skill": skill.name,
                "type": "implementation",
            },
        )

    def _render_prompt(
        self,
        prompt: str,
        variables: dict,
    ) -> str:

        pattern = re.compile(
            r"\{\{(.*?)\}\}"
        )

        def replace(
            match,
        ):

            key = match.group(
                1
            ).strip()

            return str(
                variables.get(
                    key,
                    "",
                )
            )

        return pattern.sub(
            replace,
            prompt,
        )
