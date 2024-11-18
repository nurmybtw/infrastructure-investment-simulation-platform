from fastapi import APIRouter
from typing import Dict, Union
from pydantic import BaseModel
from utils.ranking import Ranking
import pandas as pd
import numpy as np

router = APIRouter()

@router.get("/")
def get_ranking(region):
    ranking = Ranking().ranking(region)
    return ranking if ranking else { 'error': 'Not enough data available' }

@router.get("/simulation/")
def simulate_data(region):
    simulation_ranking = Ranking().simulation_ranking(region)
    return simulation_ranking if simulation_ranking else { 'error': 'Not enough data available' }

class ManualSimulationBody(BaseModel):
    region: str
    features_map: Dict[str, Union[int, float]]

@router.post("/simulation/manual/")
def simulate_data(body: ManualSimulationBody):
    region = body.region
    features_map = body.features_map
    simulation_impact = Ranking().manual_simulation(region, features_map)
    return {"impact": simulation_impact} if simulation_impact else { 'error': 'Not enough data available', 'code': 10203 }
