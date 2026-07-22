from __future__ import annotations

from pathlib import Path

from nexus.core.world_model import WorldModel
from nexus.core.event_bus import EventBus
from nexus.core.agent_registry import agent_registry

from nexus.memory.manager import memory_manager
from nexus.skills import SkillManager
from nexus.tools import tool_manager


class NexusRuntime:
    """
    Shared runtime for every Nexus agent.

    Owns all shared systems:
        • World Model
        • Event Bus
        • Memory
        • Skills
        • Tools
        • Agent Registry
    """

    def __init__(
        self,
        llm=None,
    ):

        # Core state

        self.world = WorldModel()

        self.bus = EventBus()

        self.registry = agent_registry

        # AI systems

        self.memory = memory_manager

        self.skills = SkillManager(
            llm=llm,
        )

        self.skills.load(
            Path(__file__).parent.parent
            / "skills"
            / "definitions"
        )

        self.tools = tool_manager

        # Misc

        self.config: dict = {}

        self.metadata: dict = {}

    # ----------------------------------------------------
    # Agent Management
    # ----------------------------------------------------

    def register_agent(
        self,
        agent,
    ):

        self.registry.register(agent)

    def get_agent(
        self,
        name: str,
    ):

        return self.registry.get(name)

    def ask_agent(
        self,
        name: str,
        instruction: str,
    ):

        return self.registry.execute(
            name=name,
            instruction=instruction,
        )

    # ----------------------------------------------------
    # Skills
    # ----------------------------------------------------

    def run_skill(
        self,
        skill: str,
        **kwargs,
    ):

        return self.skills.execute(
            skill,
            **kwargs,
        )

    # ----------------------------------------------------
    # Tools
    # ----------------------------------------------------

    def run_tool(
        self,
        tool: str,
        **kwargs,
    ):

        return self.tools.execute(
            tool,
            **kwargs,
        )

    # ----------------------------------------------------
    # Memory
    # ----------------------------------------------------

    def remember(
        self,
        text: str,
        metadata: dict | None = None,
    ):

        return self.memory.store(
            text=text,
            metadata=metadata or {},
        )

    def recall(
        self,
        query: str,
        limit: int = 5,
    ):

        return self.memory.search(
            query=query,
            limit=limit,
        )

    # ----------------------------------------------------
    # World
    # ----------------------------------------------------

    def update_world(
        self,
        values: dict,
    ):

        self.world.update(
            values
        )

        self.bus.publish(
            "world.updated",
            values,
        )

    def world_state(self):

        return self.world.get_state()

    # ----------------------------------------------------
    # Events
    # ----------------------------------------------------

    def publish(
        self,
        event: str,
        **payload,
    ):

        self.bus.publish(
            event,
            **payload,
        )

    def subscribe(
        self,
        event: str,
        callback,
    ):

        self.bus.subscribe(
            event,
            callback,
        )

    # ----------------------------------------------------
    # Diagnostics
    # ----------------------------------------------------

    def status(self):

        return {

            "agents": len(self.registry),

            "skills": len(
                self.skills.all()
            ),

            "tools": len(
                self.tools.all()
            ),

            "world": self.world.get_state(),

        }
