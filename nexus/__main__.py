"""Run Nexus from the command line."""

from nexus.core.event_bus import EventBus
from nexus.core.registry import AgentRegistry
from nexus.core.world_model import WorldModel
from nexus.agents.executive_agent import ExecutiveAgent
from nexus.agents.planning_agent import PlanningAgent
from nexus.agents.research_agent import ResearchAgent
from nexus.agents.finance_agent import FinanceAgent
from nexus.agents.risk_agent import RiskAgent


def main() -> None:
    world = WorldModel()
    world.update({
        'mission': 'deploy nexus',
        'goals': ['scope impact', 'allocate budget', 'mitigate risk'],
        'query': 'market analysis',
        'budget': '$50000',
        'risk': 'moderate',
    })

    bus = EventBus()
    bus.subscribe('world.updated', lambda data: print(f'World updated: {data}'))
    bus.subscribe('agent.result', lambda result: print(f'Agent emitted: {result}'))
    bus.publish('world.updated', world.get_state())

    registry = AgentRegistry()
    registry.register('executive', ExecutiveAgent())
    registry.register('planning', PlanningAgent())
    registry.register('research', ResearchAgent())
    registry.register('finance', FinanceAgent())
    registry.register('risk', RiskAgent())

    for name, agent in registry.all_agents().items():
        result = agent.execute(world.get_state())
        bus.publish('agent.result', {'agent': name, 'output': result})


if __name__ == '__main__':
    main()
