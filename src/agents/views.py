from fastapi import APIRouter
from src.agents.services import load_agents


router = APIRouter()

@router.get("/agents")
def get_agents():
    return load_agents()