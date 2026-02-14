import pandas as pd
import numpy as np
import os

def engineer_features(input_path, output_path):
    """
    Adds analytical features to the cleaned data.
    """
    print(f"Loading cleaned data from {input_path}...")
    try:
        df = pd.read_parquet(input_path)
    except FileNotFoundError:
        print(f"Error: File not found at {input_path}")
        return

    # 1. Calculate duration in minutes
    df['duration_minutes'] = (df['restored_at'] - df['reported_at']).dt.total_seconds() / 60
    
    # 2. Extract time components
    df['hour_of_day'] = df['reported_at'].dt.hour
    df['day_of_week'] = df['reported_at'].dt.day_name()
    df['is_weekend'] = df['reported_at'].dt.dayofweek >= 5
    
    # 3. Identify outliers (e.g., top 10% duration by cause)
    # A simple global outlier flag for now, typically 90th percentile
    p90_duration = df['duration_minutes'].quantile(0.90)
    df['is_long_outage'] = df['duration_minutes'] > p90_duration
    
    # 4. Asset Reliability Category (example)
    # Just a placeholder for more complex logic
    
    print(f"Saving feature-rich data to {output_path}...")
    df.to_parquet(output_path, index=False)
    print("Feature engineering complete.")
    return df

if __name__ == "__main__":
    input_file = os.path.join("data", "processed", "cleaned_outages.parquet")
    output_file = os.path.join("data", "processed", "eda_outages.parquet")
    
    engineer_features(input_file, output_file)
