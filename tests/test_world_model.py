"""
Tests for WorldModel and EventBus — the parts that don't require an API
key. Agent tests that call the LLM live in test_agents.py and are skipped
if OPENAI_API_KEY isn't set.
"""

from nexus.core.world_model import WorldModel
from nexus.core.event_bus import EventBus


def test_add_and_update_task():
    world = WorldModel(goal="Test goal", budget=1000)
    task = world.add_task(title="Do the thing", cost=100)
    assert task.status == "todo"

    world.update_task(task.id, status="done")
    assert world.tasks[task.id].status == "done"


def test_budget_math():
    world = WorldModel(budget=1000)
    line = world.add_budget_line(category="hardware", allocated=500)
    line.spent = 200
    assert world.budget_spent() == 200
    assert world.budget_remaining() == 800


def test_blocked_tasks_and_high_risks():
    world = WorldModel()
    t = world.add_task(title="Blocked thing", status="blocked")
    world.add_risk(description="Might fail", severity="high")

    assert world.blocked_tasks() == [t]
    assert len(world.high_severity_risks()) == 1


def test_event_bus_cascade():
    bus = EventBus()
    received = []

    bus.subscribe("budget.exceeded", lambda e: received.append(e.payload))
    bus.publish("budget.exceeded", remaining=-50)

    assert len(received) == 1
    assert received[0]["remaining"] == -50


def test_event_bus_wildcard():
    bus = EventBus()
    seen_kinds = []
    bus.subscribe("*", lambda e: seen_kinds.append(e.kind))

    bus.publish("task.created", task_id="t1")
    bus.publish("risk.detected", risk_id="r1")

    assert seen_kinds == ["task.created", "risk.detected"]
