from __future__ import annotations

import importlib

from .models import ToolResult
from .registry import ToolRegistry


class ToolManager:

    def __init__(self):

        self.registry = ToolRegistry()

    def register(
        self,
        tool,
    ):

        self.registry.register(
            tool
        )

    def execute(
        self,
        name: str,
        **kwargs,
    ) -> ToolResult:

        tool = self.registry.get(
            name
        )

        if tool is None:

            return ToolResult(

                success=False,

                error=f"Unknown tool '{name}'."

            )

        module = importlib.import_module(

            f"nexus.tools.implementations.{tool.implementation}"

        )

        if not hasattr(
            module,
            "execute",
        ):

            return ToolResult(

                success=False,

                error="Tool has no execute()."

            )

        result = module.execute(
            **kwargs
        )

        return ToolResult(

            success=True,

            output=result,

            metadata={

                "tool": name

            }

        )

    def all(self):

        return self.registry.all()


tool_manager = ToolManager()
