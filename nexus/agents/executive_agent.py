"""
ExecutiveAgent — "What are we trying to accomplish?"

The entry point for a raw human goal (the Intent Engine). It doesn't do
domain work itself — it delegates to the specialist agents, in order,
passing along context via the shared WorldModel. This is a simple
sequential orchestrator; a fancier version could let the model choose
which agent to call next dynamically.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.event_bus import EventBus
from nexus.core.registry import register_agent
from nexus.core.world_model import WorldModel
from nexus.agents.planning_agent import PlanningAgent
from nexus.agents.research_agent import ResearchAgent
from nexus.agents.finance_agent import FinanceAgent
from nexus.agents.risk_agent import RiskAgent


@register_agent
class ExecutiveAgent(BaseAgent):
    name = "executive_agent"
    description = (
        "You understand the overall objective and decide which specialist "
        "agent should act next. You do not do the specialist work yourself."
    )

    def __init__(self, world: WorldModel, bus: Optional[EventBus] = None, **kwargs):
        super().__init__(world, bus, **kwargs)
        # pass the same model/api_key/base_url config down to every
        # specialist agent so they all talk to the same backend
        self.planning = PlanningAgent(world, bus, **kwargs)
        self.research = ResearchAgent(world, bus, **kwargs)
        self.finance = FinanceAgent(world, bus, **kwargs)
        self.risk = RiskAgent(world, bus, **kwargs)
        self.risk.auto_subscribe()

    def bootstrap_from_goal(self, goal: str, deadline: Optional[str] = None,
                             budget: Optional[float] = None) -> list[AgentResponse]:
        """The 'Intent Engine' entry point: goal in, initial plan + budget
        out. Mirrors the design doc's first demo step."""
        self.world.goal = goal
        if deadline:
            self.world.deadline = deadline
        if budget:
            self.world.budget_total = budget

        results = []

        plan_result = self.planning.run(
            f"The project goal is: '{goal}'. Deadline: {deadline}. "
            f"Budget: {budget}. Break this into 5-8 concrete initial tasks "
            f"with owners (by role) and rough deadlines, using create_task."
        )
        results.append(plan_result)

        if budget:
            finance_result = self.finance.run(
                f"The total budget is {budget}. Based on the current tasks, "
                f"allocate it across sensible categories (e.g. hardware, "
                f"software, marketing, operations, reserve) using add_budget_line."
            )
            results.append(finance_result)

        risk_result = self.risk.run(
            "Given the current plan, identify the 2-3 most important risks "
            "to this project succeeding, with mitigations, using log_risk."
        )
        results.append(risk_result)

        return results

    def handle_event(self, description: str) -> list[AgentResponse]:
        """For step 6/7 of the demo: something goes wrong (e.g. 'our
        hardware supplier failed'). Route it to research + planning + risk
        so the plan adapts."""
        results = []

        research_result = self.research.run(
            f"Something happened: '{description}'. Note any relevant "
            f"findings or alternatives worth recording, using record_finding."
        )
        results.append(research_result)

        planning_result = self.planning.run(
            f"Something happened: '{description}'. Update the task plan "
            f"accordingly — add new tasks or change statuses as needed."
        )
        results.append(planning_result)

        return results
