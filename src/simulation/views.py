from fastapi import APIRouter
from src.simulation.core import run_simulation_steps


try:
    from .services import run_simulation
except ImportError:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from src.simulation.services import run_simulation

router = APIRouter()

@router.get("/simulation")
def get_simulation():
    graph = run_simulation()
    return {
        "nodes": list(graph.nodes(data=True))[:10],
        "edges": list(graph.edges(data=True))[:10],
    }

@router.get("/simulation/steps")
def get_simulation_steps(num_steps: int = 10):
    graph = run_simulation()
    agents = [{"id": node_id, **data} for node_id, data in graph.nodes(data=True)]
    step_results = run_simulation_steps(agents, graph, num_steps=num_steps)
    return {"steps": [
        {
            "step": r.step,
            "adopted_count": r.adopted_count,
            "total_agents": r.total_agents,
            "adopted_rate": r.adopted_rate,
            "state_distribution": r.state_distribution,
            "group_distribution": r.group_distribution,
        }
        for r in step_results
    ]}