from fastapi import APIRouter
from pydantic import BaseModel
from utils.load_excel import load_excel_data
from utils.data import Data
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from scipy.stats import linregress
import pandas as pd
import numpy as np

router = APIRouter()

@router.get("/")
def get_data(region, sector):
    data = Data().history(region, sector)
    labels = []
    values = []
    for _, row in data.iterrows():
        labels.append(row['Год'])
        values.append(row['Инвестиции'])
    return {
        'dataset': f'История инвестиции - {sector} (в млн. тенге)',
        'labels': labels,
        'values': values
    }

@router.get("/forecast/")
def predict_data(region, sector):
    years_to_predict = 5
    forecasted_data = Data().forecast(region, sector, years_to_predict)
    if forecasted_data is not None:
        labels = []
        values = []
        for _, row in forecasted_data.iterrows():
            labels.append(row['Год'])
            values.append(row['Инвестиции'])
        return {
            'dataset': f'Прогноз инвестиции - {sector} (в млн. тенге)',
            'labels': labels,
            'values': values
        }
    else:
        return {
            'error': 'Not enough data'
        }
