import pandas as pd
import os

FILE = "stored_data.csv"

def save_data(record):
    df = pd.DataFrame([record])

    if not os.path.exists(FILE):
        df.to_csv(FILE, index=False)
    else:
        df.to_csv(FILE, mode='a', header=False, index=False)