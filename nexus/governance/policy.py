from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Policy:

    name: str

    description: str = ""

    enabled: bool = True

    actions: set[str] = field(default_factory=set)

    def allows(
        self,
        action: str,
    ) -> bool:

        if not self.enabled:
            return False

        if not self.actions:
            return True

        return action in self.actions
