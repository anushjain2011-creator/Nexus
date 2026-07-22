from __future__ import annotations

from pathlib import Path

from nexus.skills import SkillManager


class BaseAgent:

    def __init__(
        self,
        runtime=None,
        llm=None,
    ):

        self.runtime = runtime
        self.llm = llm

        # ----------------------------
        # Runtime Architecture
        # ----------------------------

        if runtime is not None:

            self.world = runtime.world
            self.bus = runtime.bus
            self.memory = runtime.memory
            self.tools = runtime.tools
            self.registry = runtime.registry

            # Shared SkillManager
            self.skills = runtime.skills

        # ----------------------------
        # Standalone Mode
        # ----------------------------

        else:

            self.world = None
            self.bus = None
            self.memory = None
            self.tools = None
            self.registry = None

            self.skills = SkillManager(
                llm=llm,
            )

            self.skills.load(
                Path(__file__).parent.parent
                / "skills"
                / "definitions"
            )

    # -------------------------------------------------
    # Skills
    # -------------------------------------------------

    def run_skill(
        self,
        name: str,
        **kwargs,
    ):

        return self.skills.execute(
            name,
            **kwargs,
        )

    # -------------------------------------------------
    # Memory
    # -------------------------------------------------

    def remember(
        self,
        *args,
        **kwargs,
    ):

        if self.memory is None:
            raise RuntimeError("No runtime memory attached.")

        return self.memory.store(
            *args,
            **kwargs,
        )

    def recall(
        self,
        *args,
        **kwargs,
    ):

        if self.memory is None:
            return []

        return self.memory.search(
            *args,
            **kwargs,
        )

    # -------------------------------------------------
    # Tools
    # -------------------------------------------------

    def run_tool(
        self,
        name: str,
        **kwargs,
    ):

        if self.tools is None:
            raise RuntimeError("No ToolManager attached.")

        return self.tools.execute(
            name,
            **kwargs,
        )

    # -------------------------------------------------
    # Collaboration
    # -------------------------------------------------

    def ask_agent(
        self,
        agent: str,
        instruction: str,
    ):

        if self.registry is None:
            raise RuntimeError("No AgentRegistry attached.")

        return self.registry.execute(
            name=agent,
            instruction=instruction,
        )

    # -------------------------------------------------
    # Events
    # -------------------------------------------------

    def publish(
        self,
        event: str,
        **payload,
    ):

        if self.bus is not None:

            self.bus.publish(
                event,
                **payload,
            )
