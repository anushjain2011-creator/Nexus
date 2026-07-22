from nexus.core.agent_registry import agent_registry
from nexus.core.world_model import WorldModel
from nexus.core.event_bus import EventBus

from nexus.agents.builder import BuilderAgent
from nexus.agents.research import ResearchAgent
from nexus.agents.hiring import HiringAgent
from nexus.agents.finance import FinanceAgent


class Nexus:

    def __init__(self):

        self.world = WorldModel()

        self.bus = EventBus()

        self.builder = BuilderAgent(
            self.world,
            self.bus,
        )

        self.research = ResearchAgent(
            self.world,
            self.bus,
        )

        self.hiring = HiringAgent(
            self.world,
            self.bus,
        )

        self.finance = FinanceAgent(
            self.world,
            self.bus,
        )

        agent_registry.register(
            self.builder
        )

        agent_registry.register(
            self.research
        )

        agent_registry.register(
            self.hiring
        )

        agent_registry.register(
            self.finance
        )
