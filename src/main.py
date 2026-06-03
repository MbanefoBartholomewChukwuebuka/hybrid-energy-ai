from fastapi import FastAPI
from pydantic import BaseModel
from agent import EnergyMonitoringAgent
from database import create_table

app = FastAPI()

create_table()
agent = EnergyMonitoringAgent()

class EnergyRequest(BaseModel):
    user_id: str
    energy_kwh: float


@app.post("/analyze-energy")
def analyze_energy(request: EnergyRequest):
    return agent.analyze_energy(
        request.user_id,
        request.energy_kwh
    )


@app.get("/energy-history/{user_id}")
def history(user_id: str):
    from database import get_energy_history
    return get_energy_history(user_id)