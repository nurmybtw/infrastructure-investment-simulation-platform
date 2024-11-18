from fastapi import APIRouter
from pydantic import BaseModel
from utils.load_rating_data import load_rating_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64


router = APIRouter()

@router.get("/country/")
def get_country_rating():
    df = load_rating_data()
    df = pd.get_dummies(df, columns=["Region"], drop_first=True)

    vds_totals = df.groupby("Year")["VDS_Value"].sum().reset_index()
    df = df.merge(vds_totals, on="Year", suffixes=("", "_YearTotal"))

    region_sector_rankings = {}

    # Calculate percentage contribution for each sector across regions (one-hot encoded)
    for region_col in [col for col in df.columns if col.startswith("Region_")]:
        # Filter rows for this specific region
        region_data = df[df[region_col] == 1]
        
        # Calculate sector contribution as a percentage of the region's total VDS
        region_data["Sector_Contribution"] = region_data["VDS_Value"] / region_data["VDS_Value_YearTotal"] * 100
        
        # Calculate average contribution of each sector
        avg_contributions = region_data.groupby("Отрасль")["Sector_Contribution"].mean().sort_values(ascending=False)
        
        # Save to the rankings dictionary
        region_name = region_col.replace("Region_", "")
        region_sector_rankings[region_name] = avg_contributions

    # Convert rankings dictionary to a DataFrame for easy viewing
    rankings_df = pd.DataFrame(region_sector_rankings)
    normalized_rankings_df = rankings_df.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=0)

    plt.figure(figsize=(14, 10))
    sns.heatmap(normalized_rankings_df, annot=True, fmt=".2f", cmap="YlGnBu", cbar_kws={'label': 'Вклад (0-1)'})
    plt.title("Вклад отраслей на регионы (чем больше значение, тем больше вклада)")
    plt.xlabel("Регион")
    plt.ylabel("Отрасль")

    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close() 

    # Convert the image to base64
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return {
        "image": image_base64
    }


@router.get("/region/")
def get_region_rating(region):
    df = load_rating_data()
    df = pd.get_dummies(df, columns=["Region"], drop_first=True)

    vds_totals = df.groupby("Year")["VDS_Value"].sum().reset_index()
    df = df.merge(vds_totals, on="Year", suffixes=("", "_YearTotal"))

    region_col = f'Region_{region}'
    region_data = df[df[region_col] == 1]
    
    region_data["Sector_Contribution"] = region_data["VDS_Value"] / region_data["VDS_Value_YearTotal"] * 100
    
    top_sectors = region_data.groupby("Отрасль")["Sector_Contribution"].mean().nlargest(5).index
    
    plt.figure(figsize=(10, 6))
    for sector in top_sectors:
        sector_data = region_data[region_data["Отрасль"] == sector]
        plt.plot(sector_data["Year"], sector_data["Sector_Contribution"], label=sector)
    
    plt.title(f"Топ 5 Отраслей по вкладу в экономический рост региона {region_col.replace('Region_', '')}")
    plt.xlabel("Год")
    plt.ylabel("Вклад отрасли")
    plt.legend(title="Отрасль")
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close() 

    # Convert the image to base64
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return {
        "image": image_base64
    }
