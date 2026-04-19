import uvicorn
from fastapi import FastAPI
from src.agents.views import router as agents_router
from src.simulation.views import router as simulation_router

app = FastAPI(
    title="ABM4",
    description="Agent-Based Modeling Network for Salzburg-Heizung",
    version="1.0.0",
)


app.include_router(agents_router)
app.include_router(simulation_router)