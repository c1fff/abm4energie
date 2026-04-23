from fastapi import APIRouter
from src.agents.services import load_agents


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