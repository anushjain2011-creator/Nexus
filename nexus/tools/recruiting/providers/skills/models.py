from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SkillDefinition:

    name: str

    description: str

    prompt: str | None = None

    implementation: str | None = None

    version: str = "1.0.0"

    author: str = "Nexus"

    category: str = ""

    tags: list[str] = field(default_factory=list)

    inputs: list[str] = field(default_factory=list)

    outputs: list[str] = field(default_factory=list)

    permissions: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    enabled: bool = True

    def is_prompt(self) -> bool:

        return (
            self.prompt is not None
            and self.implementation is None
        )

    def is_implementation(self) -> bool:

        return self.implementation is not None

    def requires_permission(
        self,
        permission: str,
    ) -> bool:

        return permission in self.permissions


@dataclass(slots=True)
class SkillResult:

    success: bool

    output: Any = None

    error: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)
