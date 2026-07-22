"""
core/workflow_engine.py

Nexus Workflow Engine

Coordinates execution between:
- Planner
- Scheduler
- TaskQueue
- Registry
- EventBus

The workflow engine converts execution plans into
running agent workflows.
"""

from __future__ import annotations

import asyncio
from typing import Dict, Any, List, Optional


class WorkflowEngine:

    def __init__(
        self,
        planner,
        scheduler,
        registry,
        event_bus,
        world_model,
    ):
        self.planner = planner
        self.scheduler = scheduler
        self.registry = registry
        self.event_bus = event_bus
        self.world_model = world_model

        self.running_workflows = {}

    # ---------------------------------------------------------

    async def execute_goal(
        self,
        goal: str,
    ) -> str:
        """
        Bootstrap a goal into a workflow.

        Returns workflow id.
        """

        self.planner.bootstrap_goal(goal)

        workflow_id = self.world_model.generate_id()

        self.running_workflows[workflow_id] = {
            "goal": goal,
            "status": "planning",
            "completed": [],
            "failed": [],
        }

        self.planner.create_schedule(self.scheduler)

        self.running_workflows[workflow_id]["status"] = "running"

        await self.event_bus.publish(
            event="workflow.started",
            payload={
                "workflow_id": workflow_id,
                "goal": goal,
            },
            source="WorkflowEngine",
        )

        return workflow_id

    # ---------------------------------------------------------

    async def tick(self):

        await self.scheduler.tick()

    # ---------------------------------------------------------

    async def execute_ready_tasks(self):

        completed = set()

        for workflow in self.running_workflows.values():

            completed.update(workflow["completed"])

        ready = self.planner.ready_tasks(completed)

        for task in ready:

            agent_cls = self.registry.get_agent(task.agent)

            agent = agent_cls(
                world_model=self.world_model,
                event_bus=self.event_bus,
                registry=self.registry,
            )

            async def runner(agent=agent, task=task):

                await self.event_bus.publish(
                    event="task.started",
                    payload={
                        "task": task.name,
                        "agent": task.agent,
                    },
                    source="WorkflowEngine",
                )

                result = await agent.execute(
                    goal=task.goal,
                    context=task.metadata,
                )

                self.scheduler.mark_completed(task.id)

                await self.event_bus.publish(
                    event="task.completed",
                    payload={
                        "task": task.name,
                        "result": result,
                    },
                    source="WorkflowEngine",
                )

                return result

            await self.scheduler.task_queue.submit(
                task_id=task.id,
                name=task.name,
                func=runner,
                priority=task.priority,
            )

    # ---------------------------------------------------------

    async def monitor(self):

        while True:

            await self.tick()

            await self.execute_ready_tasks()

            await asyncio.sleep(0.25)

    # ---------------------------------------------------------

    async def cancel_workflow(
        self,
        workflow_id: str,
    ):

        if workflow_id not in self.running_workflows:
            return

        self.running_workflows[workflow_id]["status"] = "cancelled"

        await self.event_bus.publish(
            event="workflow.cancelled",
            payload={
                "workflow_id": workflow_id,
            },
            source="WorkflowEngine",
        )

    # ---------------------------------------------------------

    async def finish_workflow(
        self,
        workflow_id: str,
    ):

        if workflow_id not in self.running_workflows:
            return

        self.running_workflows[workflow_id]["status"] = "completed"

        await self.event_bus.publish(
            event="workflow.completed",
            payload={
                "workflow_id": workflow_id,
            },
            source="WorkflowEngine",
        )

    # ---------------------------------------------------------

    def workflow_status(
        self,
        workflow_id: str,
    ):

        return self.running_workflows.get(workflow_id)

    # ---------------------------------------------------------

    def active_workflows(self):

        return {
            k: v
            for k, v in self.running_workflows.items()
            if v["status"] == "running"
        }

    # ---------------------------------------------------------

    def summary(self):

        return {
            "running": len(self.active_workflows()),
            "total": len(self.running_workflows),
        }
