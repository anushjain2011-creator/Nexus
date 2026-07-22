"""Run Nexus."""

from nexus.core.event_bus import EventBus
from nexus.core.world_model import WorldModel
from nexus.core.agent_registry import agent_registry

from nexus.agents.executive_agent import ExecutiveAgent
from nexus.agents.planning_agent import PlanningAgent
from nexus.agents.research_agent import ResearchAgent
from nexus.agents.finance_agent import FinanceAgent
from nexus.agents.risk_agent import RiskAgent


def main() -> None:

    world = WorldModel()

    world.update(
        {
            "mission": "Deploy Nexus",
            "goals": [
                "Scope impact",
                "Allocate budget",
                "Mitigate risk",
            ],
            "query": "Market analysis",
            "budget": "$50,000",
            "risk": "Moderate",
        }
    )

    bus = EventBus()

    bus.subscribe(
        "world.updated",
        lambda data: print(f"[WORLD] {data}"),
    )

    bus.subscribe(
        "agent.result",
        lambda data: print(f"[RESULT] {data}"),
    )

    executive = ExecutiveAgent(
        world,
        bus,
    )

    planning = PlanningAgent(
        world,
        bus,
    )

    research = ResearchAgent(
        world,
        bus,
    )

    finance = FinanceAgent(
        world,
        bus,
    )

    risk = RiskAgent(
        world,
        bus,
    )

    agent_registry.register(
        executive,
    )

    agent_registry.register(
        planning,
    )

    agent_registry.register(
        research,
    )

    agent_registry.register(
        finance,
    )

    agent_registry.register(
        risk,
    )

    bus.publish(
        "world.updated",
        world.get_state(),
    )

    result = executive.run(
        "Create a deployment strategy for Nexus."
    )

    print("\n===== FINAL RESPONSE =====\n")
    print(result.summary)


if __name__ == "__main__":
    main()
