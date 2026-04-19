from fastapi import APIRouter, Query
from src.simulation.core import run_simulation_steps


try:
    from .services import run_simulation
except ImportError:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from src.simulation.services import run_simulation

router = APIRouter(tags=["simulation"], prefix="/simulation")

@router.get("/simulation/steps")
def get_simulation_steps(
    num_steps: int = 10,
    municipality: str = Query(None, description="Filter by municipality"),
    p_unaware: float = Query(0.01, description="Base adoption probability for UNAWARE state"),
    p_aware: float = Query(0.15, description="Base adoption probability for AWARE state"),
    alpha: float = Query(0.4, description="Spatial component weight"),
    beta: float = Query(0.3, description="Homophily component weight"),
    gamma: float = Query(0.3, description="Influence component weight"),
):
    """
    Run adoption simulation with configurable parameters.
    
    Parameters:
    - num_steps: Number of simulation steps (default 10)
    - municipality: Optional municipality filter
    - p_unaware: Base adoption probability for UNAWARE agents (default 0.01)
    - p_aware: Base adoption probability for AWARE agents (default 0.15)
    - alpha: Spatial weight in edge calculation (default 0.4)
    - beta: Homophily weight in edge calculation (default 0.3)
    - gamma: Influence weight in edge calculation (default 0.3)
    """
    graph = run_simulation()
    
    # Filter by municipality if specified
    if municipality:
        nodes_in_municipality = [
            node_id for node_id, data in graph.nodes(data=True)
            if data.get("municipality") == municipality
        ]
        graph = graph.subgraph(nodes_in_municipality).copy()
    
    agents = [{"id": node_id, **data} for node_id, data in graph.nodes(data=True)]
    step_results = run_simulation_steps(
        agents,
        graph,
        num_steps=num_steps,
        p_unaware=p_unaware,
        p_aware=p_aware,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
    )
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