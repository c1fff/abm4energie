from fastapi import APIRouter, Query, HTTPException
from src.simulation.core import run_simulation_steps
from src.simulation.sessions import store_session, session_exists, get_session, sessions

try:
    from .services import run_simulation
except ImportError:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from src.simulation.services import run_simulation

router = APIRouter(tags=["simulation"], prefix="/simulation")

@router.get("/steps")
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
    step_results, agent_history = run_simulation_steps(
        agents,
        graph,
        num_steps=num_steps,
        p_unaware=p_unaware,
        p_aware=p_aware,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
    )
    
    # Store session and get session_id
    session_id = store_session(graph, agent_history)

    if municipality:
        return {
            "session_id": session_id,
            "municipality": municipality,
            "agents": agents,
            "edges": [{"source": u, "target": v, **data} for u, v, data in graph.edges(data=True)],
            "steps": [
                {
                    "step": r.step,
                    "adopted_count": r.adopted_count,
                    "total_agents": r.total_agents,
                    "adopted_rate": r.adopted_rate,
                    "state_distribution": r.state_distribution,
                    "group_distribution": r.group_distribution,
                }
                for r in step_results
            ],
        }


    return {
        "session_id": session_id,
        "steps": [
            {
                "step": r.step,
                "adopted_count": r.adopted_count,
                "total_agents": r.total_agents,
                "adopted_rate": r.adopted_rate,
                "state_distribution": r.state_distribution,
                "group_distribution": r.group_distribution,
            }
            for r in step_results
        ]
    }


@router.get("/agent/{agent_id}")
def get_agent_history(agent_id: int, session_id: str = Query(..., description="Session ID from /steps response")):
    """
    Get detailed history of a specific agent from a saved session.
    
    Parameters:
    - agent_id: ID of the agent to retrieve history for
    - session_id: Session ID from the /steps endpoint response
    
    Returns:
    - Agent history with adoption probability, state changes, and neighbor influence for each step
    """
    # Check if session exists
    if not session_exists(session_id):
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    session = get_session(session_id)
    agent_history = session.get("agent_history", {})
    graph = session.get("graph")
    
    # Check if agent exists in the session
    if agent_id not in agent_history:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found in session {session_id}")
    
    # Get agent metadata from graph
    agent_data = {}
    if graph and agent_id in graph.nodes:
        agent_data = dict(graph.nodes[agent_id])
    
    return {
        "agent_id": agent_id,
        "municipality": agent_data.get("municipality", "Unknown"),
        "steps": agent_history[agent_id]
    }


@router.get("/sessions/debug")
def debug_sessions():
    """
    Debug endpoint to view all active sessions and their agent counts.
    (Development only)
    """
    session_list = []
    for sid, data in sessions.items():
        agent_history = data.get("agent_history", {})
        session_list.append({
            "session_id": sid,
            "agent_count": len(agent_history),
            "timestamp": data.get("timestamp")
        })
    
    return {
        "total_sessions": len(sessions),
        "max_sessions": 20,
        "sessions": session_list
    }