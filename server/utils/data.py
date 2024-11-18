import pandas as pd
import numpy as np
import os
import glob
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pandas as pd
import numpy as np


class Data:
    def __init__(self) -> None:
        pass

    def load_gdp_data(self):
        path = os.path.join('data/gdp/', 'gdp.xlsx')
        gdp_data = pd.read_excel(path)
        gdp_data.iloc[:, 1:] = gdp_data.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
        deflator = gdp_data.iloc[-1, 1:]
        gdp_data.iloc[:-1, 1:] = gdp_data.iloc[:-1, 1:].div(deflator, axis=1) * 100 * 0.001
        gdp_data = gdp_data[:-1]
        gdp_data = gdp_data.melt(id_vars=['Регион'], var_name='Год', value_name='ВВП')
        gdp_data['ВВП_прош'] = gdp_data.groupby("Регион")["ВВП"].shift(1)
        return gdp_data
    
    def load_investment_data(self):
        investment_files = glob.glob(os.path.join('./data/investment/', "*.xlsx"))
        all_data = []

        for file in investment_files:
            year = file.split('\\')[-1].replace('.xlsx', '')
            df = pd.read_excel(file)
            df['Год'] = int(year)
            df = df.melt(id_vars=['Год', 'Отрасль'], var_name='Регион', value_name='Инвестиции')
            all_data.append(df)

        investment_data = pd.concat(all_data, ignore_index=True)
        investment_data["Отрасль"] = investment_data["Отрасль"].replace({
            "Водоснабжение; водоотведение; сбор, обработка и удаление отходов, деятельность по ликвидации загрязнений": "Водоснабжение; сбор, обработка и удаление отходов, деятельность по ликвидации загрязнений",
        })
        investment_data['Инвестиции'] = investment_data['Инвестиции'].apply(pd.to_numeric, errors='coerce') * 0.001
        return investment_data

    def load_data(self):
        gdp_data = self.load_gdp_data()
        investment_data = self.load_investment_data()
        merged = pd.merge(investment_data, gdp_data, on=['Год', 'Регион'], how='inner')
        return merged
    
    def history(self, region, sector):
        data = self.load_data()
        filtered_data = data.loc[
            (data['Регион'] == region) & 
            (data['Отрасль'] == sector)
        ]
        return filtered_data
    
    def forecast(self, region, sector, years_to_predict):
        data = self.load_data()
        filtered_data = data.loc[
            (data['Регион'] == region) & 
            (data['Отрасль'] == sector)
        ]
        filtered_data = filtered_data.set_index("Год")
        # filtered_data = filtered_data.dropna().astype(float)
        if len(filtered_data) > 2:
            model = ExponentialSmoothing(filtered_data["Инвестиции"], trend="add", seasonal=None)
            fit = model.fit()
            smoothed_values = fit.fittedvalues
            forecast_years = list(range(2024, 2024 + 5))
            forecast = fit.forecast(steps=years_to_predict)
            forecast.index = forecast_years 
            combined = pd.concat([smoothed_values, forecast])
            combined.index.name = "Год"
            combined_df = combined.reset_index()
            combined_df.columns = ["Год", "Инвестиции"]
            return combined_df
        else:
            return None