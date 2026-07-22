"""
core/scheduler.py

Nexus Scheduler

Responsible for:
- Scheduling queued tasks
- Dependency checking
- Delayed execution
- Priorities
- Deadline awareness
"""

from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ScheduledTask:

    id: str

    name: str

    agent: str

    goal: str

    priority: int = 5

    execute_at: float = field(default_factory=lambda: time.time())

    deadline: Optional[float] = None

    dependencies: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    status: str = "scheduled"


class Scheduler:

    def __init__(self, task_queue):

        self.task_queue = task_queue

        self.tasks: Dict[str, ScheduledTask] = {}

        self.running = False

        self.interval = 0.5

    # --------------------------------------------------

    async def start(self):

        self.running = True

        while self.running:

            await self.tick()

            await asyncio.sleep(self.interval)

    # --------------------------------------------------

    async def stop(self):

        self.running = False

    # --------------------------------------------------

    async def tick(self):

        now = time.time()

        for task in list(self.tasks.values()):

            if task.status != "scheduled":
                continue

            if task.execute_at > now:
                continue

            if not self.dependencies_met(task):
                continue

            await self.dispatch(task)

    # --------------------------------------------------

    def dependencies_met(self, task: ScheduledTask):

        for dependency in task.dependencies:

            if dependency not in self.tasks:
                return False

            if self.tasks[dependency].status != "completed":
                return False

        return True

    # --------------------------------------------------

    async def dispatch(self, task: ScheduledTask):

        async def runner():

            task.status = "running"

            return {
                "agent": task.agent,
                "goal": task.goal,
                "metadata": task.metadata,
            }

        await self.task_queue.submit(
            task_id=task.id,
            name=task.name,
            func=runner,
            priority=task.priority,
        )

        task.status = "completed"

    # --------------------------------------------------

    def schedule(
        self,
        *,
        name: str,
        agent: str,
        goal: str,
        priority: int = 5,
        delay: float = 0,
        deadline: Optional[float] = None,
        dependencies=None,
        metadata=None,
    ):

        dependencies = dependencies or []

        metadata = metadata or {}

        task = ScheduledTask(
            id=str(uuid.uuid4()),
            name=name,
            agent=agent,
            goal=goal,
            priority=priority,
            execute_at=time.time() + delay,
            deadline=deadline,
            dependencies=dependencies,
            metadata=metadata,
        )

        self.tasks[task.id] = task

        return task

    # --------------------------------------------------

    def mark_completed(self, task_id):

        if task_id in self.tasks:

            self.tasks[task_id].status = "completed"

    # --------------------------------------------------

    def mark_failed(self, task_id):

        if task_id in self.tasks:

            self.tasks[task_id].status = "failed"

    # --------------------------------------------------

    def get(self, task_id):

        return self.tasks.get(task_id)

    # --------------------------------------------------

    def all(self):

        return self.tasks

    # --------------------------------------------------

    def pending(self):

        return [
            t
            for t in self.tasks.values()
            if t.status == "scheduled"
        ]

    # --------------------------------------------------

    def completed(self):

        return [
            t
            for t in self.tasks.values()
            if t.status == "completed"
        ]

    # --------------------------------------------------

    def failed(self):

        return [
            t
            for t in self.tasks.values()
            if t.status == "failed"
        ]

    # --------------------------------------------------

    def overdue(self):

        now = time.time()

        overdue = []

        for task in self.tasks.values():

            if (
                task.deadline is not None
                and task.deadline < now
                and task.status != "completed"
            ):
                overdue.append(task)

        return overdue

    # --------------------------------------------------

    def summary(self):

        return {
            "total": len(self.tasks),
            "scheduled": len(self.pending()),
            "completed": len(self.completed()),
            "failed": len(self.failed()),
            "overdue": len(self.overdue()),
        }
