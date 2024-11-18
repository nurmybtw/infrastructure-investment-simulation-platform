from fastapi import APIRouter
from pydantic import BaseModel
from utils.load_excel import load_excel_data
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from scipy.stats import linregress
import pandas as pd
import numpy as np

router = APIRouter()



@router.get("/")
def get_data(region):
    realestate_data = load_excel_data('Инвестиции в жилищное строительство.xlsx')
    return {
        'dataset': 'Инвестиции в жилищное строительство',
        'labels': realestate_data.columns[1:].values.tolist(),
        'values': realestate_data[realestate_data['Region'] == region]
            .iloc[:, 1:]
            .values
            .flatten()
            .tolist()
    }

@router.get("/forecast/")
def predict_data(region):
    realestate_data = load_excel_data('Инвестиции в жилищное строительство.xlsx')
    realestate_data.set_index('Region', inplace=True)

    forecast_steps = 5
    all_years = list(realestate_data.columns) + [i+2023 for i in range(1, forecast_steps + 1)]
    df_smooth_forecast = pd.DataFrame(columns=['Region'] + all_years)
    df_smooth_forecast['Region'] = realestate_data.index

    region_data = realestate_data.loc[region].dropna().astype(float)
    
    # Exponential Smoothing model
    model = ExponentialSmoothing(region_data, trend='add', seasonal=None)
    model_fit = model.fit()

    # Smoothed and forecasted values
    smoothed_values = model_fit.fittedvalues.reindex(realestate_data.columns, fill_value=np.nan)
    forecast_values = model_fit.forecast(steps=forecast_steps)

    # Combine smoothed and forecasted values
    combined_series = pd.concat([smoothed_values, forecast_values])
    df_smooth_forecast.loc[df_smooth_forecast['Region'] == region, all_years] = combined_series.values
    
    slope, intercept, _, _, _ = linregress(range(len(smoothed_values)), smoothed_values)
    return {
        'dataset': f'Инвестиции в жилищное строительство (Прогноз)',
        'labels': df_smooth_forecast.columns[1:].values.tolist(),
        'values': df_smooth_forecast[df_smooth_forecast['Region'] == region]
            .iloc[:, 1:]
            .dropna(axis=1, how='all')
            .values
            .flatten()
            .tolist(),
        'growth_rate': slope
    }
