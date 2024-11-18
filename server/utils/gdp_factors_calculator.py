import pandas as pd

########################################################################
# Dataset Loader
# Put it into some __init__ maybe, in order to upload it once only
########################################################################

gdp_data = pd.read_excel('/content/drive/MyDrive/geospatialAI/gdp/gdp.xlsx')
gdp_data.iloc[:, 1:] = gdp_data.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
deflator = gdp_data.iloc[-1, 1:]
gdp_data.iloc[:-1, 1:] = gdp_data.iloc[:-1, 1:].div(deflator, axis=1) * 100 * 1000
gdp_data = gdp_data[:-1]
gdp_data = gdp_data.melt(id_vars=['Регион'], var_name='Год', value_name='ВВП')

population_data = pd.read_excel('/content/drive/MyDrive/geospatialAI/population/population.xlsx')
population_data.iloc[:, 1:] = population_data.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
population_data = population_data.melt(id_vars=['Регион'], var_name='Год', value_name='Население')

investment_files = glob.glob(os.path.join('/content/drive/MyDrive/geospatialAI/investment/', "*.xlsx"))

# Initialize an empty list to store each year's data
all_data = []

# Loop over each file and load it
for file in investment_files:
    # Extract the year from the filename (assuming it’s in the filename, e.g., 'data_2020.xlsx')
    year = file.split('/')[-1].replace('.xlsx', '')
    # Load the Excel file into a DataFrame
    df = pd.read_excel(file)
    
    # Add a 'Year' column
    df['Год'] = int(year)
    
    # Melt the DataFrame to make it long-format: one row per sector, region, and year
    df = df.melt(id_vars=['Год', 'Отрасль'], var_name='Регион', value_name='Инвестиции')
    
    # Append the processed DataFrame to the list
    all_data.append(df)

# Concatenate all years' data into a single DataFrame
investment_data = pd.concat(all_data, ignore_index=True)
investment_data["Отрасль"] = investment_data["Отрасль"].replace({
    "Водоснабжение; водоотведение; сбор, обработка и удаление отходов, деятельность по ликвидации загрязнений": "Водоснабжение; сбор, обработка и удаление отходов, деятельность по ликвидации загрязнений",
})
investment_data['Инвестиции'] = investment_data['Инвестиции'].apply(pd.to_numeric, errors='coerce')

investment_data = investment_data.pivot_table(index=['Год', 'Регион'], columns='Отрасль', values='Инвестиции', fill_value=0)
investment_data.reset_index(inplace=True)

merged = pd.merge(investment_data, population_data, on=['Год', 'Регион'], how='inner')
merged = pd.merge(merged, gdp_data, on=['Год', 'Регион'], how='inner')


# Step 1: Data Cleaning
# Ensure GDP and Year are numerical
merged['ВВП'] = pd.to_numeric(merged['ВВП'], errors='coerce')  # Convert ВВП to numeric
merged['Год'] = pd.to_numeric(merged['Год'], errors='coerce')  # Convert Year to numeric

from sklearn.ensemble import RandomForestRegressor

########################################################################
# Prediction part
# Checks all the previous data, fits the RandomForestRegressor, and for each region makes some recommendation
# Put it into some main function
########################################################################

# Step 1: Prepare the dataset
# Group data by region
regions = merged['Регион'].unique()

# Dictionary to store recommendations for each region
recommendations = {}

# Step 2: Train a model and analyze feature importance for each region
for region in regions:
    # Filter data for the specific region
    region_data = merged[merged['Регион'] == region]
    
    # Separate features (X) and target (y)
    X_region = region_data.drop(['Год', 'Регион', 'ВВП'], axis=1)
    y_region = region_data['ВВП']
    
    # Check if there are enough data points for the region
    if len(region_data) < 5:
        print(f"Not enough data for region: {region}")
        continue
    
    # Step 3: Train a Random Forest Regressor for the region
    rf_region = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_region.fit(X_region, y_region)
    
    # Step 4: Analyze Feature Importance
    feature_importance_region = pd.DataFrame({
        'Feature': X_region.columns,
        'Importance': rf_region.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    
    # Identify top 3 variables to focus on for increasing GDP
    top_features = feature_importance_region.head(3)
    
########################################################################
# {top_features} is what you need
# Decide how many top_features (currently 3 is shown) and display for each region with real-time calculations
########################################################################

    # Store recommendations
    recommendations[region] = top_features[['Feature', 'Importance']]
    print(f"\nTop recommendations for {region}:")
    print(top_features)
    
    
    # Optional: Simulate impact by increasing top features by 10% (as previously discussed)
    X_region_increased = X_region.copy()
    for feature in top_features['Feature']:
        X_region_increased[feature] *= 1.1  # Simulate a 10% increase
    
    # Predict the GDP increase with simulated changes
    y_pred_original = rf_region.predict(X_region)
    y_pred_increased = rf_region.predict(X_region_increased)
    impact = y_pred_increased.mean() - y_pred_original.mean()
    print(f"Predicted impact on ВВП with a 10% increase in top variables: {impact}\n")

########################################################################
# Last 3 code blocks display how it will effect the GDP if we increase each of the topN variables by 10%
########################################################################
