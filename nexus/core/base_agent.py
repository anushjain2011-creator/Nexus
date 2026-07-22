"""Base agent class for Nexus."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping

class BaseAgent(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def act(self, context: Mapping[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def execute(self, context: Mapping[str, Any]) -> dict[str, Any]:
        result = self.act(context)
        if not isinstance(result, dict):
            raise TypeError('Agent.act must return a dict')
        return result
