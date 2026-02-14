import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid
import random
import os

def generate_data(n=1000, seed=42):
    """
    Generates synthetic outage data.
    """
    np.random.seed(seed)
    random.seed(seed)

    regions = ['London', 'South East', 'East Anglia']
    causes = ['weather', 'asset_failure', 'third_party', 'unknown']
    asset_types = ['cable', 'transformer', 'overhead_line']
    priorities = ['emergency', 'high', 'normal']

    data = []
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 1, 1)
    range_days = (end_date - start_date).days

    for _ in range(n):
        incident_id = str(uuid.uuid4())
        
        # Random reporting time
        days_offset = random.randint(0, range_days)
        seconds_offset = random.randint(0, 86400)
        reported_at = start_date + timedelta(days=days_offset, seconds=seconds_offset)

        # Duration based on cause (simplified logic for correlation)
        cause = np.random.choice(causes, p=[0.3, 0.4, 0.2, 0.1])
        
        if cause == 'weather':
            duration_minutes = int(np.random.exponential(scale=120)) # Average 2 hours
        elif cause == 'asset_failure':
            duration_minutes = int(np.random.exponential(scale=240)) # Average 4 hours
        else:
            duration_minutes = int(np.random.exponential(scale=60)) # Average 1 hour
            
        # Ensure minimum duration of 1 minute
        duration_minutes = max(1, duration_minutes)
        
        restored_at = reported_at + timedelta(minutes=duration_minutes)

        region = np.random.choice(regions)
        asset_type = np.random.choice(asset_types)
        priority = np.random.choice(priorities)
        
        # Customers affected - heavy tail distribution
        customers_affected = int(np.random.lognormal(mean=3, sigma=1.5))
        
        # Planned outages
        planned = np.random.choice([True, False], p=[0.1, 0.9])
        
        if planned:
            # Planned outages usually have round numbers and specific durations, but keeping it simple
            priority = 'normal'
            cause = 'maintenance' if np.random.random() > 0.5 else 'upgrade'
            # Adjust duration for planned?
            
        data.append({
            'incident_id': incident_id,
            'reported_at': reported_at,
            'restored_at': restored_at,
            'region': region,
            'cause': cause,
            'asset_type': asset_type,
            'customers_affected': customers_affected,
            'priority': priority,
            'planned': planned
        })

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    output_path = os.path.join("data", "raw", "outages.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print("Generating synthetic data...")
    df = generate_data(n=5000)
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")
    print(df.head())
