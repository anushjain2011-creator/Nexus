"""World model for Nexus."""

from __future__ import annotations

from typing import Any

class WorldModel:
    def __init__(self) -> None:
        self.state: dict[str, Any] = {}

    def update(self, data: dict[str, Any]) -> None:
        if not isinstance(data, dict):
            raise TypeError('WorldModel.update requires a dict')
        self.state.update(data)

    def get_state(self) -> dict[str, Any]:
        return dict(self.state)

    def clear(self) -> None:
        self.state.clear()
