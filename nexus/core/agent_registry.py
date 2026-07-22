from __future__ import annotations

from typing import Iterator

from .base_agent import BaseAgent


class AgentRegistry:

    def __init__(self):

        self._agents: dict[str, BaseAgent] = {}

    def register(
        self,
        agent: BaseAgent,
    ):

        self._agents[agent.name] = agent

        agent.set_agent_registry(
            self
        )

    def unregister(
        self,
        name: str,
    ):

        self._agents.pop(
            name,
            None,
        )

    def get(
        self,
        name: str,
    ):

        return self._agents.get(
            name
        )

    def names(
        self,
    ):

        return sorted(
            self._agents.keys()
        )

    def all(
        self,
    ):

        return list(
            self._agents.values()
        )

    def execute(
        self,
        name: str,
        instruction: str,
        **kwargs,
    ):

        agent = self.get(
            name
        )

        if agent is None:

            raise ValueError(
                f"Unknown agent '{name}'."
            )

        return agent.run(
            instruction,
            **kwargs,
        )

    def broadcast(
        self,
        instruction: str,
        exclude: set[str] | None = None,
    ):

        exclude = exclude or set()

        results = {}

        for name, agent in self._agents.items():

            if name in exclude:

                continue

            results[name] = agent.run(
                instruction
            )

        return results

    def __contains__(
        self,
        name: str,
    ):

        return name in self._agents

    def __len__(
        self,
    ):

        return len(
            self._agents
        )

    def __iter__(
        self,
    ) -> Iterator[BaseAgent]:

        return iter(
            self._agents.values()
        )


agent_registry = AgentRegistry()
