"""
core/planner.py

Nexus Planner

Responsible for:
- Converting goals into executable tasks
- Building dependency graphs (DAG)
- Detecting dependency cycles
- Topological sorting
- Critical path estimation
- Producing execution plans for the Scheduler
"""

from __future__ import annotations

from dataclasses import dataclass, field
from collections import defaultdict, deque
from typing import Dict, List, Optional, Set


# ---------------------------------------------------------
# Task Model
# ---------------------------------------------------------

@dataclass
class PlanTask:
    id: str
    name: str
    agent: str
    goal: str

    duration: int = 1

    priority: int = 5

    dependencies: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)


# ---------------------------------------------------------
# Planner
# ---------------------------------------------------------

class Planner:

    def __init__(self):

        self.tasks: Dict[str, PlanTask] = {}

    # -----------------------------------------------------

    def add_task(self, task: PlanTask):

        self.tasks[task.id] = task

    # -----------------------------------------------------

    def remove_task(self, task_id: str):

        if task_id in self.tasks:
            del self.tasks[task_id]

    # -----------------------------------------------------

    def get_task(self, task_id):

        return self.tasks.get(task_id)

    # -----------------------------------------------------

    def clear(self):

        self.tasks.clear()

    # -----------------------------------------------------
    # Dependency Graph
    # -----------------------------------------------------

    def dependency_graph(self):

        graph = defaultdict(list)

        indegree = defaultdict(int)

        for task in self.tasks.values():

            indegree.setdefault(task.id, 0)

            for dep in task.dependencies:

                graph[dep].append(task.id)

                indegree[task.id] += 1

        return graph, indegree

    # -----------------------------------------------------
    # Cycle Detection
    # -----------------------------------------------------

    def has_cycles(self):

        graph, indegree = self.dependency_graph()

        queue = deque()

        for node, degree in indegree.items():

            if degree == 0:

                queue.append(node)

        visited = 0

        while queue:

            node = queue.popleft()

            visited += 1

            for nxt in graph[node]:

                indegree[nxt] -= 1

                if indegree[nxt] == 0:

                    queue.append(nxt)

        return visited != len(self.tasks)

    # -----------------------------------------------------
    # Topological Sort
    # -----------------------------------------------------

    def execution_order(self):

        if self.has_cycles():

            raise RuntimeError(
                "Planner detected dependency cycle."
            )

        graph, indegree = self.dependency_graph()

        queue = deque()

        for node, degree in indegree.items():

            if degree == 0:

                queue.append(node)

        order = []

        while queue:

            node = queue.popleft()

            order.append(self.tasks[node])

            for nxt in graph[node]:

                indegree[nxt] -= 1

                if indegree[nxt] == 0:

                    queue.append(nxt)

        return order

    # -----------------------------------------------------
    # Critical Path
    # -----------------------------------------------------

    def critical_path_duration(self):

        order = self.execution_order()

        longest: Dict[str, int] = {}

        for task in order:

            if not task.dependencies:

                longest[task.id] = task.duration

            else:

                longest[task.id] = max(
                    longest[d]
                    for d in task.dependencies
                ) + task.duration

        if not longest:

            return 0

        return max(longest.values())

    # -----------------------------------------------------
    # Ready Tasks
    # -----------------------------------------------------

    def ready_tasks(self, completed: Set[str]):

        ready = []

        for task in self.tasks.values():

            if task.id in completed:
                continue

            ok = True

            for dep in task.dependencies:

                if dep not in completed:

                    ok = False
                    break

            if ok:

                ready.append(task)

        return ready

    # -----------------------------------------------------
    # Scheduler Integration
    # -----------------------------------------------------

    def create_schedule(self, scheduler):

        plan = self.execution_order()

        ids = []

        for task in plan:

            scheduled = scheduler.schedule(
                name=task.name,
                agent=task.agent,
                goal=task.goal,
                priority=task.priority,
                dependencies=task.dependencies,
                metadata=task.metadata,
            )

            ids.append(scheduled.id)

        return ids

    # -----------------------------------------------------
    # Automatic Goal Decomposition
    # -----------------------------------------------------

    def bootstrap_goal(
        self,
        goal: str,
        agent: str = "planning",
    ):

        """
        Placeholder decomposition.

        Later the PlanningAgent can replace this
        with LLM-generated milestones.
        """

        self.clear()

        root = PlanTask(
            id="discover",
            name="Understand Goal",
            goal=goal,
            agent=agent,
        )

        research = PlanTask(
            id="research",
            name="Research",
            goal=goal,
            agent="research",
            dependencies=["discover"],
        )

        plan = PlanTask(
            id="plan",
            name="Create Plan",
            goal=goal,
            agent="planning",
            dependencies=["research"],
        )

        execute = PlanTask(
            id="execute",
            name="Execute Plan",
            goal=goal,
            agent="executive",
            dependencies=["plan"],
        )

        review = PlanTask(
            id="review",
            name="Review Outcome",
            goal=goal,
            agent="analytics",
            dependencies=["execute"],
        )

        self.add_task(root)
        self.add_task(research)
        self.add_task(plan)
        self.add_task(execute)
        self.add_task(review)

    # -----------------------------------------------------

    def summary(self):

        return {
            "tasks": len(self.tasks),
            "critical_path": self.critical_path_duration(),
            "cycle": self.has_cycles(),
            "execution_order": [
                t.name
                for t in self.execution_order()
            ] if not self.has_cycles() else [],
        }
