import pandas as pd
import numpy as np
import os

def compute_metrics(input_path):
    """
    Computes key outage metrics.
    """
    print(f"Loading feature data from {input_path}...")
    try:
        df = pd.read_parquet(input_path)
    except FileNotFoundError:
        print(f"Error: File not found at {input_path}")
        return

    metrics = {}

    # 1. Volume
    metrics['total_incidents'] = len(df)
    metrics['incidents_per_day'] = df.groupby(df['reported_at'].dt.date).size().mean()
    
    # 2. Impact
    metrics['total_customers_affected'] = df['customers_affected'].sum()
    metrics['median_customers_affected'] = df['customers_affected'].median()
    metrics['p90_customers_affected'] = df['customers_affected'].quantile(0.90)

    # 3. Response Performance
    metrics['median_restoration_time'] = df['duration_minutes'].median()
    metrics['p90_restoration_time'] = df['duration_minutes'].quantile(0.90)
    
    # 4. Breakdowns (calculating but not printing all to keep it clean)
    by_cause = df.groupby('cause')['duration_minutes'].median()
    by_asset = df.groupby('asset_type')['duration_minutes'].median()
    
    print("\n--- Key Metrics ---")
    print(f"Total Incidents: {metrics['total_incidents']}")
    print(f"Total Customers Affected: {metrics['total_customers_affected']}")
    print(f"Median Restoration Time: {metrics['median_restoration_time']:.2f} min")
    print(f"P90 Restoration Time: {metrics['p90_restoration_time']:.2f} min")
    
    print("\n--- Median Restoration by Cause ---")
    print(by_cause)
    
    return metrics, by_cause, by_asset

if __name__ == "__main__":
    input_file = os.path.join("data", "processed", "eda_outages.parquet")
    compute_metrics(input_file)
