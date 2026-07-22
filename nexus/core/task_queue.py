"""
core/task_queue.py

Asynchronous task queue for Nexus.

Supports:
- Priority scheduling
- Async execution
- Retries
- Cancellation
- Worker pool
"""

from __future__ import annotations

import asyncio
import itertools
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, Optional


TaskCallable = Callable[..., Awaitable[Any]]


@dataclass(order=True)
class QueueTask:
    priority: int
    order: int

    id: str = field(compare=False)

    name: str = field(compare=False)

    func: TaskCallable = field(compare=False)

    args: tuple = field(default_factory=tuple, compare=False)

    kwargs: Dict[str, Any] = field(default_factory=dict, compare=False)

    retries: int = field(default=0, compare=False)

    max_retries: int = field(default=3, compare=False)

    status: str = field(default="queued", compare=False)

    result: Any = field(default=None, compare=False)

    error: Optional[str] = field(default=None, compare=False)


class TaskQueue:

    def __init__(self, workers: int = 4):

        self.workers = workers

        self.queue = asyncio.PriorityQueue()

        self.tasks: Dict[str, QueueTask] = {}

        self.counter = itertools.count()

        self.running = False

        self.worker_tasks = []

    # --------------------------------------------------------

    async def start(self):

        if self.running:
            return

        self.running = True

        for i in range(self.workers):

            worker = asyncio.create_task(self._worker(i))

            self.worker_tasks.append(worker)

    # --------------------------------------------------------

    async def stop(self):

        self.running = False

        for w in self.worker_tasks:

            w.cancel()

        self.worker_tasks.clear()

    # --------------------------------------------------------

    async def submit(
        self,
        *,
        task_id: str,
        name: str,
        func: TaskCallable,
        priority: int = 10,
        args=(),
        kwargs=None,
        max_retries=3,
    ):

        kwargs = kwargs or {}

        task = QueueTask(
            priority=priority,
            order=next(self.counter),
            id=task_id,
            name=name,
            func=func,
            args=args,
            kwargs=kwargs,
            max_retries=max_retries,
        )

        self.tasks[task_id] = task

        await self.queue.put(task)

        return task

    # --------------------------------------------------------

    async def _worker(self, worker_id):

        while self.running:

            task: QueueTask = await self.queue.get()

            try:

                task.status = "running"

                task.result = await task.func(
                    *task.args,
                    **task.kwargs,
                )

                task.status = "completed"

            except Exception as e:

                task.error = str(e)

                if task.retries < task.max_retries:

                    task.retries += 1

                    task.status = "retrying"

                    await self.queue.put(task)

                else:

                    task.status = "failed"

            finally:

                self.queue.task_done()

    # --------------------------------------------------------

    async def join(self):

        await self.queue.join()

    # --------------------------------------------------------

    def cancel(self, task_id: str):

        if task_id in self.tasks:

            self.tasks[task_id].status = "cancelled"

    # --------------------------------------------------------

    def status(self, task_id: str):

        task = self.tasks.get(task_id)

        if task is None:

            return None

        return {
            "id": task.id,
            "name": task.name,
            "status": task.status,
            "priority": task.priority,
            "retries": task.retries,
            "result": task.result,
            "error": task.error,
        }

    # --------------------------------------------------------

    def all_tasks(self):

        return {
            k: self.status(k)
            for k in self.tasks
        }

    # --------------------------------------------------------

    def queued(self):

        return [
            t.id
            for t in self.tasks.values()
            if t.status == "queued"
        ]

    # --------------------------------------------------------

    def running_tasks(self):

        return [
            t.id
            for t in self.tasks.values()
            if t.status == "running"
        ]

    # --------------------------------------------------------

    def completed(self):

        return [
            t.id
            for t in self.tasks.values()
            if t.status == "completed"
        ]

    # --------------------------------------------------------

    def failed(self):

        return [
            t.id
            for t in self.tasks.values()
            if t.status == "failed"
        ]
