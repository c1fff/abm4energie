try:
    from .network import build_agent_graph
    from ..agents.services import load_agents
except ImportError:
    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(project_root))
    from src.simulation.network import build_agent_graph
    from src.agents.services import load_agents


def run_simulation():
    agents = load_agents()
    graph = build_agent_graph(agents)
    return graph
