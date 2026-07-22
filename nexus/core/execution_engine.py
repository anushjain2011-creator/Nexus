"""
core/execution_engine.py

Top-level execution engine for Nexus.

Coordinates:

    WorkflowEngine
    Planner
    Scheduler
    TaskQueue
    EventBus
    WorldModel

This is the entrypoint used by the ExecutiveAgent.
"""

from __future__ import annotations

import asyncio
from typing import Dict, Optional


class ExecutionEngine:

    def __init__(
        self,
        planner,
        scheduler,
        workflow_engine,
        task_queue,
        world_model,
        event_bus,
    ):

        self.planner = planner
        self.scheduler = scheduler
        self.workflow_engine = workflow_engine
        self.task_queue = task_queue
        self.world_model = world_model
        self.event_bus = event_bus

        self.running = False

        self.monitor_task = None

    # -----------------------------------------------------
    # Startup
    # -----------------------------------------------------

    async def start(self):

        if self.running:
            return

        self.running = True

        await self.task_queue.start()

        self.monitor_task = asyncio.create_task(
            self._main_loop()
        )

        await self.event_bus.publish(
            event="engine.started",
            payload={},
            source="ExecutionEngine",
        )

    # -----------------------------------------------------

    async def stop(self):

        if not self.running:
            return

        self.running = False

        if self.monitor_task:

            self.monitor_task.cancel()

        await self.task_queue.stop()

        await self.event_bus.publish(
            event="engine.stopped",
            payload={},
            source="ExecutionEngine",
        )

    # -----------------------------------------------------

    async def _main_loop(self):

        while self.running:

            await self.workflow_engine.tick()

            await self.workflow_engine.execute_ready_tasks()

            await asyncio.sleep(0.25)

    # -----------------------------------------------------
    # Execute Goal
    # -----------------------------------------------------

    async def execute_goal(
        self,
        goal: str,
    ) -> str:

        workflow = await self.workflow_engine.execute_goal(goal)

        return workflow

    # -----------------------------------------------------
    # Execute Existing Plan
    # -----------------------------------------------------

    async def execute_plan(self):

        self.planner.create_schedule(
            self.scheduler
        )

    # -----------------------------------------------------
    # Wait Until Everything Finishes
    # -----------------------------------------------------

    async def wait(self):

        await self.task_queue.join()

    # -----------------------------------------------------
    # Cancel Workflow
    # -----------------------------------------------------

    async def cancel_workflow(
        self,
        workflow_id: str,
    ):

        await self.workflow_engine.cancel_workflow(
            workflow_id
        )

    # -----------------------------------------------------
    # Emergency Stop
    # -----------------------------------------------------

    async def emergency_stop(self):

        self.running = False

        await self.task_queue.stop()

        await self.event_bus.publish(
            event="engine.emergency_stop",
            payload={},
            source="ExecutionEngine",
        )

    # -----------------------------------------------------
    # Restart
    # -----------------------------------------------------

    async def restart(self):

        await self.stop()

        await self.start()

    # -----------------------------------------------------
    # Health
    # -----------------------------------------------------

    def health(self):

        return {
            "running": self.running,
            "queued_tasks": len(
                self.task_queue.queued()
            ),
            "running_tasks": len(
                self.task_queue.running_tasks()
            ),
            "completed_tasks": len(
                self.task_queue.completed()
            ),
            "failed_tasks": len(
                self.task_queue.failed()
            ),
            "scheduler": self.scheduler.summary(),
            "planner": self.planner.summary(),
            "workflow_engine": self.workflow_engine.summary(),
        }

    # -----------------------------------------------------
    # Snapshot
    # -----------------------------------------------------

    def snapshot(self):

        return {
            "world": self.world_model.snapshot(),
            "engine": self.health(),
        }

    # -----------------------------------------------------
    # Status
    # -----------------------------------------------------

    def status(self):

        return {
            "running": self.running,
            "health": self.health(),
        }

    # -----------------------------------------------------
    # Event Injection
    # -----------------------------------------------------

    async def inject_event(
        self,
        event: str,
        payload: Optional[Dict] = None,
    ):

        payload = payload or {}

        await self.event_bus.publish(
            event=event,
            payload=payload,
            source="ExecutionEngine",
        )

    # -----------------------------------------------------
    # World Access
    # -----------------------------------------------------

    def world(self):

        return self.world_model

    # -----------------------------------------------------

    def __repr__(self):

        return (
            "<ExecutionEngine "
            f"running={self.running}>"
        )
