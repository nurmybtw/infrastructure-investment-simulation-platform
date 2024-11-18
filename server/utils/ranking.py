import pandas as pd
import numpy as np
import os
import glob
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np

class Ranking:
    def __init__(self):
        data = self.load_data()
        self.regions = data['Регион'].unique()
        self.models = {}
        self.data = {}
        # Step 2: Train a model and analyze feature importance for each region
        # Filter data for the specific region
        for region in self.regions:
            region_data = data[data['Регион'] == region]
            # Separate features (X) and target (y)
            X_region = region_data.drop(['Год', 'Регион', 'ВВП'], axis=1)
            y_region = region_data['ВВП']
            
            # Check if there are enough data points for the region
            if len(region_data) < 5: continue
            
            # Step 3: Train a Random Forest Regressor for the region
            rf_region = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_region.fit(X_region, y_region)
            self.models[region] = rf_region
            self.data[region] = (X_region, y_region)
            

    def load_gdp_data(self):
        path = os.path.join('data/gdp/', 'gdp.xlsx')
        gdp_data = pd.read_excel(path)
        gdp_data.iloc[:, 1:] = gdp_data.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
        deflator = gdp_data.iloc[-1, 1:]
        gdp_data.iloc[:-1, 1:] = gdp_data.iloc[:-1, 1:].div(deflator, axis=1) * 100 * 1000
        gdp_data = gdp_data[:-1]
        gdp_data = gdp_data.melt(id_vars=['Регион'], var_name='Год', value_name='ВВП')
        return gdp_data
    
    def load_population_data(self):
        path = os.path.join('data/population/', 'population.xlsx')
        population_data = pd.read_excel(path)
        population_data.iloc[:, 1:] = population_data.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
        population_data = population_data.melt(id_vars=['Регион'], var_name='Год', value_name='Население')
        return population_data
    
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
        investment_data['Инвестиции'] = investment_data['Инвестиции'].apply(pd.to_numeric, errors='coerce') * 0.000001
        investment_data = investment_data.pivot_table(index=['Год', 'Регион'], columns='Отрасль', values='Инвестиции', fill_value=0)
        investment_data.reset_index(inplace=True)
        return investment_data
    
    def load_data(self):
        gdp_data = self.load_gdp_data()
        population_data = self.load_population_data()
        investment_data = self.load_investment_data()
        # merged = pd.merge(investment_data, population_data, on=['Год', 'Регион'], how='inner')
        merged = pd.merge(investment_data, gdp_data, on=['Год', 'Регион'], how='inner')
        # Step 1: Data Cleaning
        # Ensure GDP and Year are numerical
        merged['ВВП'] = pd.to_numeric(merged['ВВП'], errors='coerce') * 0.000001
        merged['Год'] = pd.to_numeric(merged['Год'], errors='coerce')
        return merged
    
    
    def ranking(self, region):
        if region not in self.models:
            return None
        rf_region = self.models[region]
        X_region, y_region = self.data[region]
        
        # Step 4: Analyze Feature Importance
        feature_importance_region = pd.DataFrame({
            'Feature': X_region.columns,
            'Importance': rf_region.feature_importances_
        }).sort_values(by='Importance', ascending=False)
        return {
            row[1]['Feature']: row[1]['Importance'] 
            for row in feature_importance_region.iterrows()
        }
        # top_features = feature_importance_region.head(3)
    
    def simulation_ranking(self, region):
        if region not in self.models:
            return None
        X_region, y_region = self.data[region]
        rf_region = self.models[region]
        impacts = {}
        for feature in X_region.columns:
            X_region_increased = X_region.copy()
            X_region_increased[feature] *= 1.1  # Simulate a 10% increase
            # Predict the GDP increase with simulated changes
            y_pred_original = rf_region.predict(X_region)
            y_pred_increased = rf_region.predict(X_region_increased)
            impact = y_pred_increased.mean() - y_pred_original.mean()
            impacts[feature] = impact
        return dict(sorted(impacts.items(), key=lambda item: item[1], reverse=True))
    
    def manual_simulation(self, region, features_map):
        if region not in self.models:
            return None
        X_region, y_region = self.data[region]
        rf_region = self.models[region]
        X_region_increased = X_region.copy()
        for feature in features_map:
            X_region_increased[feature] *= features_map[feature]
            # Predict the GDP increase with simulated changes
        y_pred_original = rf_region.predict(X_region)
        y_pred_increased = rf_region.predict(X_region_increased)
        impact = y_pred_increased.mean() - y_pred_original.mean()
        return impact

            