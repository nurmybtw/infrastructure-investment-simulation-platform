import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

def load_vds_files(folder_path):
    vds_data = []
    for file_path in glob.glob(os.path.join(folder_path, "vds_*.xlsx")):
        
        year = int(file_path.split("_")[-1].split(".")[0])
        df = pd.read_excel(file_path)
        
        df_melted = df.melt(id_vars=["Отрасль"], var_name="Region", value_name="VDS_Value")
        df_melted["Year"] = year
        
        vds_data.append(df_melted)
    
    return pd.concat(vds_data, ignore_index=True)

def load_gdp_file(gdp_file_path):
    gdp_df = pd.read_excel(os.path.join(gdp_file_path, "gdp.xlsx"))
    gdp_df_long = gdp_df.melt(id_vars=["Год"], var_name="Region", value_name="GDP")
    gdp_df_long = gdp_df_long.rename(columns={"Год": "Year"})
    
    return gdp_df_long

def create_lagged_features(df, lag_years=1):
    df = df.sort_values(by=["Region", "Year"]).reset_index(drop=True)
    # lagged features (gdp)
    for lag in range(1, lag_years + 1):
        df[f"GDP_Lag{lag}"] = df.groupby("Region")["GDP"].shift(lag)
        
    return df

def load_rating_data():
    vds_folder_path = "data"
    vds_df = load_vds_files(vds_folder_path)
    sphere_mapping = {
        "Снабжение электроэнергией, газом, паром, горячей водой и кондиционированным воздухом": "Электроснабжение, подача газа, пара и воздушное кондиционирование",
        "Водоснабжение сбор, обработка и удаление отходов; деятельность поликвидации загрязнений": "Водоснабжение; канализационная система, контроль над сбором и распределением отходов",
        "Здравоохранение и социальное обслуживание населения": "Здравоохранение и социальные услуги"
    }
    vds_df["Отрасль"] = vds_df["Отрасль"].replace(sphere_mapping)
    city_mapping = {
        "г. Нур-Султан": "г. Астана",
        "Карагандиская": "Карагандинская"
    }
    vds_df["Region"] = vds_df["Region"].replace(city_mapping)

    gdp_file_path = "data"
    gdp_df = load_gdp_file(gdp_file_path)
    gdp_df = gdp_df.dropna()
    gdp_df["Region"] = gdp_df["Region"].replace(city_mapping)
    gdp_df = create_lagged_features(gdp_df, lag_years=1)

    merged_df = pd.merge(vds_df, gdp_df, on=["Year", "Region"], how="left")

    return merged_df