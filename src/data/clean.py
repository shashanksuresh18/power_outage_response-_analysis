import pandas as pd
import numpy as np
import os

def clean_data(input_path, output_path):
    """
    Cleans the raw outage data.
    """
    print(f"Loading data from {input_path}...")
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: File not found at {input_path}")
        return

    # 1. Ensure correct data types
    df['incident_id'] = df['incident_id'].astype(str)
    df['reported_at'] = pd.to_datetime(df['reported_at'], errors='coerce')
    df['restored_at'] = pd.to_datetime(df['restored_at'], errors='coerce')
    
    # 2. Drop rows with missing critical dates
    df.dropna(subset=['reported_at', 'restored_at'], inplace=True)
    
    # 3. Handle duplicates
    initial_rows = len(df)
    df.drop_duplicates(subset=['incident_id'], inplace=True)
    dropped_rows = initial_rows - len(df)
    if dropped_rows > 0:
        print(f"Dropped {dropped_rows} duplicate rows.")

    # 4. Filter invalid durations (restored before reported)
    invalid_dates = df[df['restored_at'] < df['reported_at']]
    if not invalid_dates.empty:
        print(f"Found {len(invalid_dates)} records with restored_at < reported_at. Dropping them.")
        df = df[df['restored_at'] >= df['reported_at']]

    # 5. Ensure categorical consistency (simple check)
    df['region'] = df['region'].astype('category')
    df['cause'] = df['cause'].astype('category')
    df['asset_type'] = df['asset_type'].astype('category')
    df['priority'] = df['priority'].astype('category')

    print(f"Saving cleaned data to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(output_path, index=False)
    print("Data cleaning complete.")
    return df

if __name__ == "__main__":
    input_file = os.path.join("data", "raw", "outages.csv")
    output_file = os.path.join("data", "processed", "cleaned_outages.parquet")
    
    clean_data(input_file, output_file)
