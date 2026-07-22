from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SkillDefinition:

    name: str

    description: str

    prompt: str | None = None

    implementation: str | None = None

    tags: list[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)
