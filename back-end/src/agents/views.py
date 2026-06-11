from fastapi import APIRouter
from src.agents.services import decision_score, load_agents


router = APIRouter(tags=["agents"], prefix="/agents")

@router.get("/agents")
def get_agents():
    return load_agents()

@router.get("/agents/municipalities")
def get_municipalities():
    agents = load_agents()
    municipalities = {}
    for agent in agents:
        if agent.municipality not in municipalities:
            municipalities[agent.municipality] = []
        municipalities[agent.municipality].append(agent.id)
    return municipalities   

@router.get("/agents/income")
def get_income_groups():
    agents = load_agents()
    income_groups = {}
    for agent in agents:
        if agent.income is None or agent.income == "No Information":
            income_groups["No Information"] = income_groups.get("No Information", 0) + 1
        else:
            income_groups[agent.income] = income_groups.get(agent.income, 0) + 1
    return income_groups

@router.get("/agents/current_state")
def get_agents_current_state_by_id(id: int):
    agents = load_agents()
    for agent in agents:
        if agent.id == id:
            return {"id": agent.id, "current_state": agent.state}
    return {"error": "Agent not found"}


@router.get("/{agent_id}/decision_score")
def get_agent_decision_score(agent_id: int):
    agents = load_agents()
    for agent in agents:
        if agent.id == agent_id:
            return {
                "agent_id": agent.id,
                "foerderung": agent.foerderung,
                "trigger": agent.trigger,
                "social_influence": agent.social_influence,
                "info_sources": agent.info_sources,
                "known_households": agent.known_households,
                "decision_score": decision_score(agent),
            }
    return {"error": "Agent not found"}
