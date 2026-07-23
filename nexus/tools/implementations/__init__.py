from .manager import ToolManager, tool_manager
from .models import ToolDefinition, ToolResult
from .registry import ToolRegistry, tool_registry

__all__ = [
    "ToolDefinition",
    "ToolResult",
    "ToolRegistry",
    "ToolManager",
    "tool_registry",
    "tool_manager",
]

# Built-in tools — each name maps to a module in nexus/tools/implementations/
# that exposes execute(method, **kwargs).
_BUILTIN_TOOLS = [
    ToolDefinition(
        name="github",
        description="Create/read GitHub issues and repos.",
        implementation="github",
    ),
    ToolDefinition(
        name="jira",
        description="Read and search Jira issues.",
        implementation="jira",
    ),
    ToolDefinition(
        name="notion",
        description="Read Notion pages and databases.",
        implementation="notion",
    ),
    ToolDefinition(
        name="slack",
        description="Send Slack messages.",
        implementation="slack",
    ),
    ToolDefinition(
        name="stripe",
        description="Read/create Stripe customers and payments.",
        implementation="stripe",
    ),
    ToolDefinition(
        name="calendar",
        description="Create calendar events.",
        implementation="calendar",
    ),
    ToolDefinition(
        name="email",
        description="Send email.",
        implementation="email",
    ),
]

for _tool in _BUILTIN_TOOLS:
    tool_manager.register(_tool)
