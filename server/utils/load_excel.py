import pandas as pd
import numpy as np
import os

def load_excel_data(file_name):
    file_path = os.path.join("data", file_name)
    realestate_investments = pd.read_excel(file_path)
    realestate_investments.replace('-', np.nan, inplace=True)
    realestate_investments.iloc[:, 1:] = realestate_investments.iloc[:, 1:].apply(
        pd.to_numeric, 
        errors='coerce'
    )
    return realestate_investments
