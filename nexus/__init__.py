"""
Nexus — The Execution Operating System
Core package exposing the agent framework.
"""

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.world_model import WorldModel
from nexus.core.event_bus import EventBus, Event

__all__ = [
    "BaseAgent",
    "AgentResponse",
    "WorldModel",
    "EventBus",
    "Event",
]

__version__ = "0.1.0"
