import pytest
import pandas as pd
import numpy as np
import os
from src.data.clean import clean_data

@pytest.fixture
def raw_data(tmp_path):
    # Create sample raw data
    data = {
        'incident_id': ['1', '2', '3', '1'], # Duplicate ID
        'reported_at': ['2023-01-01 10:00:00', '2023-01-01 11:00:00', 'invalid_date', '2023-01-01 10:00:00'],
        'restored_at': ['2023-01-01 12:00:00', '2023-01-01 09:00:00', '2023-01-01 12:00:00', '2023-01-01 12:00:00'], # 2nd is invalid (restored before reported)
        'region': ['London', 'South East', 'East Anglia', 'London'],
        'cause': ['weather', 'unknown', 'weather', 'weather'],
        'asset_type': ['cable', 'cable', 'cable', 'cable'],
        'priority': ['high', 'high', 'high', 'high'],
        'customers_affected': [100, 200, 300, 100]
    }
    df = pd.DataFrame(data)
    input_path = tmp_path / "raw.csv"
    df.to_csv(input_path, index=False)
    return str(input_path)

def test_clean_data(raw_data, tmp_path):
    output_path = str(tmp_path / "cleaned.parquet")
    
    # Run cleaning
    cleaned_df = clean_data(raw_data, output_path)
    
    # Assertions
    assert len(cleaned_df) == 1 # Only incident '1' is valid
    # Incident '2' dropped because restored < reported
    # Incident '3' dropped because invalid reported_at
    # Duplicate '1' dropped
    
    assert cleaned_df.iloc[0]['incident_id'] == '1'
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df['reported_at'])
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df['restored_at'])
    
    # Check categorical conversion
    assert cleaned_df['region'].dtype.name == 'category'

def test_missing_file():
    assert clean_data("non_existent.csv", "output.parquet") is None
