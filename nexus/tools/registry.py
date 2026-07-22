from __future__ import annotations

from .models import ToolDefinition


class ToolRegistry:

    def __init__(self):

        self._tools: dict[
            str,
            ToolDefinition,
        ] = {}

    def register(
        self,
        tool: ToolDefinition,
    ):

        self._tools[
            tool.name
        ] = tool

    def register_many(
        self,
        tools: list[ToolDefinition],
    ):

        for tool in tools:

            self.register(
                tool
            )

    def get(
        self,
        name: str,
    ):

        return self._tools.get(
            name
        )

    def all(self):

        return list(
            self._tools.values()
        )

    def clear(self):

        self._tools.clear()


tool_registry = ToolRegistry()
