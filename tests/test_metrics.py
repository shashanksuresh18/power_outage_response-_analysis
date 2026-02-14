import pytest
import pandas as pd
import numpy as np
from src.metrics.compute import compute_metrics

@pytest.fixture
def processed_data(tmp_path):
    # Create sample processed data
    data = {
        'incident_id': ['1', '2', '3', '4', '5'],
        'reported_at': pd.to_datetime(['2023-01-01']*5),
        'duration_minutes': [10, 20, 30, 40, 100], # Median=30, P90 depends on method
        'customers_affected': [100, 100, 100, 100, 1000],
        'cause': ['A', 'A', 'B', 'B', 'C'],
        'asset_type': ['X', 'X', 'Y', 'Y', 'Z']
    }
    df = pd.DataFrame(data)
    input_path = tmp_path / "processed.parquet"
    df.to_parquet(input_path, index=False)
    return str(input_path)

def test_compute_metrics(processed_data):
    metrics, by_cause, by_asset = compute_metrics(processed_data)
    
    assert metrics['total_incidents'] == 5
    assert metrics['total_customers_affected'] == 1400
    assert metrics['median_restoration_time'] == 30.0
    
    # P90 of [10, 20, 30, 40, 100] is roughly 76 depending on interpolation
    # Pandas quantile default is linear
    p90 = pd.Series([10, 20, 30, 40, 100]).quantile(0.9)
    assert metrics['p90_restoration_time'] == p90
    
    # Check groupings
    assert by_cause['A'] == 15.0 # Median of 10, 20
    assert by_asset['Z'] == 100.0

def test_missing_file():
    assert compute_metrics("non_existent.parquet") is None
