"""
Minimal end-to-end demo matching the "robotics startup" walkthrough:

  1. Give the ExecutiveAgent a goal -> it delegates to Planning/Finance/Risk
     to bootstrap the project (Intent Engine).
  2. Print the resulting WorldModel.
  3. Simulate a problem ("hardware supplier failed") and show the agents
     adapting the plan.

Run with:
    cp .env.example .env   # fill in OPENAI_API_KEY / OPENAI_BASE_URL / OPENAI_MODEL
    python examples/run_demo.py
"""

from dotenv import load_dotenv
load_dotenv()

from nexus.core.world_model import WorldModel
from nexus.core.event_bus import EventBus
from nexus.agents.executive_agent import ExecutiveAgent


def main() -> None:
    world = WorldModel()
    bus = EventBus()
    exec_agent = ExecutiveAgent(world, bus)

    print("=== Step 1: Bootstrap from goal ===")
    results = exec_agent.bootstrap_from_goal(
        goal="Build a robotics startup with 4 people and a $5,000 budget",
        deadline="30 days",
        budget=5000,
    )
    for r in results:
        print(f"\n[{r.agent_name}] {r.summary}")

    print("\n=== World state after bootstrap ===")
    print(world.summary_for_prompt())

    print("\n=== Step 2: Something goes wrong ===")
    results = exec_agent.handle_event("Our hardware supplier just failed.")
    for r in results:
        print(f"\n[{r.agent_name}] {r.summary}")

    print("\n=== World state after adaptation ===")
    print(world.summary_for_prompt())

    print("\n=== Full world model (JSON) ===")
    print(world.to_json())


if __name__ == "__main__":
    main()
