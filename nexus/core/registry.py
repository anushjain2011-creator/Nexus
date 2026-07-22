"""Agent registry for Nexus."""

from __future__ import annotations

from typing import Any

class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, Any] = {}

    def register(self, name: str, agent: Any) -> None:
        self._agents[name] = agent

    def deregister(self, name: str) -> None:
        self._agents.pop(name, None)

    def get(self, name: str) -> Any:
        return self._agents.get(name)

    def all_agents(self) -> dict[str, Any]:
        return dict(self._agents)
