"""
ExecutiveAgent — Nexus CEO

The Executive never performs specialist work itself.
It creates a plan, delegates work to registered agents,
collects results, and returns a unified response.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.registry import register_agent


@register_agent
class ExecutiveAgent(BaseAgent):

    name = "executive"

    description = (
        "Coordinates specialist agents to accomplish user goals."
    )

    def __init__(
        self,
        runtime=None,
        **kwargs,
    ):

        super().__init__(
            runtime=runtime,
            **kwargs,
        )

    # ---------------------------------------------------------
    # Bootstrap a new project
    # ---------------------------------------------------------

    def bootstrap_from_goal(
        self,
        goal: str,
        deadline: Optional[str] = None,
        budget: Optional[float] = None,
    ) -> list[AgentResponse]:

        if self.world:

            self.world.goal = goal

            if deadline:
                self.world.deadline = deadline

            if budget:
                self.world.budget_total = budget

        tasks = []

        tasks.append({
            "agent": "planning_agent",
            "instruction": (
                f"""
                Project Goal: {goal}

                Deadline: {deadline}

                Budget: {budget}

                Break this into 5-8 concrete tasks.
                """
            ),
        })

        if budget is not None:

            tasks.append({
                "agent": "finance_agent",
                "instruction": (
                    f"""
                    Budget available:

                    {budget}

                    Allocate across categories.
                    """
                ),
            })

        tasks.append({
            "agent": "risk_agent",
            "instruction": (
                """
                Review the project.

                Identify the three largest risks.

                Suggest mitigations.
                """
            ),
        })

        return self.execute_plan(tasks)

    # ---------------------------------------------------------
    # Handle unexpected events
    # ---------------------------------------------------------

    def handle_event(
        self,
        description: str,
    ) -> list[AgentResponse]:

        tasks = [

            {
                "agent": "research_agent",
                "instruction": (
                    f"""
                    Something happened:

                    {description}

                    Research alternatives.
                    """
                ),
            },

            {
                "agent": "planning_agent",
                "instruction": (
                    f"""
                    Something happened:

                    {description}

                    Update the project plan.
                    """
                ),
            },

            {
                "agent": "risk_agent",
                "instruction": (
                    f"""
                    Something happened:

                    {description}

                    Update the project risks.
                    """
                ),
            },

        ]

        return self.execute_plan(tasks)

    # ---------------------------------------------------------
    # Generic orchestration
    # ---------------------------------------------------------

    def execute_plan(
        self,
        tasks: list[dict],
    ) -> list[AgentResponse]:

        results = []

        for task in tasks:

            result = self.ask_agent(
                task["agent"],
                task["instruction"],
            )

            results.append(result)

        return results
