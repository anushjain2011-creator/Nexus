"""Run Nexus."""

from nexus.core.runtime import NexusRuntime

from nexus.agents.executive_agent import ExecutiveAgent
from nexus.agents.planning_agent import PlanningAgent
from nexus.agents.research_agent import ResearchAgent
from nexus.agents.finance_agent import FinanceAgent
from nexus.agents.risk_agent import RiskAgent


def main() -> None:

    runtime = NexusRuntime()

    runtime.world.update(
        {
            "goal": "Deploy Nexus",
            "deadline": None,
            "budget": 50000.0,
        }
    )

    runtime.bus.subscribe(
        "world.updated",
        lambda event: print(f"[WORLD] {event.payload}"),
    )

    runtime.bus.subscribe(
        "agent.result",
        lambda event: print(f"[RESULT] {event.payload}"),
    )

    executive = ExecutiveAgent(runtime)
    planning = PlanningAgent(runtime)
    research = ResearchAgent(runtime)
    finance = FinanceAgent(runtime)
    risk = RiskAgent(runtime)

    runtime.register_agent(executive)
    runtime.register_agent(planning)
    runtime.register_agent(research)
    runtime.register_agent(finance)
    runtime.register_agent(risk)

    runtime.bus.publish(
        "world.updated",
        **runtime.world.get_state(),
    )

    result = executive.run(
        "Create a deployment strategy for Nexus."
    )

    print("\n===== FINAL RESPONSE =====\n")
    print(result.summary)


if __name__ == "__main__":
    main()
