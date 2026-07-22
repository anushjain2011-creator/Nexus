from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ToolDefinition:

    name: str

    description: str

    implementation: str

    version: str = "1.0.0"

    author: str = "Nexus"

    category: str = ""

    permissions: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    enabled: bool = True


@dataclass(slots=True)
class ToolResult:

    success: bool

    output: Any = None

    error: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)
