"""Tests for Nexus agents."""

from nexus.agents.executive_agent import ExecutiveAgent
from nexus.agents.planning_agent import PlanningAgent
from nexus.agents.research_agent import ResearchAgent
from nexus.agents.finance_agent import FinanceAgent
from nexus.agents.risk_agent import RiskAgent


def test_agent_execution_returns_dict():
    context = {
        'mission': 'demo',
        'goals': ['test'],
        'query': 'test',
        'budget': '$1000',
        'risk': 'low',
    }

    agents = [
        ExecutiveAgent(),
        PlanningAgent(),
        ResearchAgent(),
        FinanceAgent(),
        RiskAgent(),
    ]

    for agent in agents:
        result = agent.execute(context)
        assert isinstance(result, dict)
        assert result.get('role') is not None
