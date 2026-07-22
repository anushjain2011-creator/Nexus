"""
Tests for Nexus agent wiring — verifies agents construct correctly and
declare valid tool schemas, without making real LLM calls (no API key
required). Behavior that requires an actual model response is exercised
manually via examples/run_demo.py or the dashboard instead.
"""

import pytest

from nexus.core.world_model import WorldModel
from nexus.core.event_bus import EventBus
from nexus.core.registry import AgentRegistry
from nexus.agents.planning_agent import PlanningAgent
from nexus.agents.research_agent import ResearchAgent
from nexus.agents.finance_agent import FinanceAgent
from nexus.agents.risk_agent import RiskAgent


@pytest.fixture
def world():
    return WorldModel(goal="Test goal", budget=1000)


@pytest.fixture
def bus():
    return EventBus()


def test_agents_registered():
    expected = {
        "planning_agent",
        "research_agent",
        "finance_agent",
        "risk_agent",
        "executive_agent",
    }
    assert expected.issubset(set(AgentRegistry.available()))


def test_planning_agent_tool_schema(world, bus):
    agent = PlanningAgent(world, bus, api_key="test-key")
    names = {t["name"] for t in agent.tools()}
    assert names == {"create_task", "update_task_status"}


def test_finance_agent_tool_handles_spend(world, bus):
    agent = FinanceAgent(world, bus, api_key="test-key")
    result = agent.handle_tool_call(
        "add_budget_line", {"category": "hardware", "allocated": 500}
    )
    assert result["status"] == "created"

    spend_result = agent.handle_tool_call(
        "record_spend", {"category": "hardware", "amount": 200}
    )
    assert spend_result["spent"] == 200
    assert world.budget_remaining() == 800


def test_finance_agent_publishes_budget_exceeded(world, bus):
    received = []
    bus.subscribe("budget.exceeded", lambda e: received.append(e.payload))

    agent = FinanceAgent(world, bus, api_key="test-key")
    agent.handle_tool_call(
        "record_spend", {"category": "hardware", "amount": 5000}
    )

    assert len(received) == 1


def test_risk_agent_logs_risk(world, bus):
    agent = RiskAgent(world, bus, api_key="test-key")
    result = agent.handle_tool_call(
        "log_risk", {"description": "Supplier may fail", "severity": "high"}
    )
    assert result["status"] == "logged"
    assert len(world.high_severity_risks()) == 1


def test_research_agent_records_finding(world, bus):
    agent = ResearchAgent(world, bus, api_key="test-key")
    agent.handle_tool_call(
        "record_finding", {"note": "Motor X is cheaper than Motor Y"}
    )
    assert len(world.knowledge) == 1
    assert "Motor X" in world.knowledge[0]["note"]
