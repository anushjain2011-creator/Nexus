"""
AgentRegistry — lets the orchestrator (or the marketplace, eventually)
discover agents by name instead of importing each one directly. Agents
register themselves via the @register_agent decorator.
"""

from __future__ import annotations

from typing import Type

from nexus.core.base_agent import BaseAgent


class AgentClassRegistry:
    _agents: dict[str, Type[BaseAgent]] = {}

    @classmethod
    def register(cls, agent_cls: Type[BaseAgent]) -> Type[BaseAgent]:
        cls._agents[agent_cls.name] = agent_cls
        return agent_cls

    @classmethod
    def get(cls, name: str) -> Type[BaseAgent]:
        if name not in cls._agents:
            raise KeyError(
                f"No agent registered as '{name}'. Available: "
                f"{list(cls._agents.keys())}"
            )
        return cls._agents[name]

    @classmethod
    def available(cls) -> list[str]:
        return list(cls._agents.keys())


def register_agent(agent_cls: Type[BaseAgent]) -> Type[BaseAgent]:
    """Decorator form: @register_agent above a BaseAgent subclass."""
    return AgentClassRegistry.register(agent_cls)
