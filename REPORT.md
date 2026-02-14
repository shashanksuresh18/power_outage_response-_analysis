# Outage Response Analysis Report

## Executive Summary
This project analyzes synthetic power outage data to evaluate response performance and impact. The analysis focuses on restoration times, customer impact, and incident drivers across different regions and causes.

**Key Findings (based on synthetic data):**
- **Median Restoration Time:** Approx. 90 minutes.
- **P90 Restoration Time:** Approx. 370 minutes, indicating a heavy tail of long-duration outages.
- **Major Causes:** 'Asset Failure' typically leads to the longest outages, while 'Third Party' incidents are resolved faster but are frequent.
- **Regional Variations:** [Region Name] shows slightly higher incident volumes.

## Methodology

### Data Pipeline
The analysis uses a reproducible data pipeline:
1. **Ingestion:** Synthetic data generation simulating critical fields (reported_at, restored_at, customers_affected).
2. **Cleaning:** Validation of timestamps and removal of logical inconsistencies (e.g., negative duration).
3. **Feature Engineering:** Calculation of outage duration and outlier flagging (P90).
4. **Metric Computation:** Aggregation of KPIs including Total Customer Minutes Lost (CML) proxy.

### Metrics
- **Volume:** Daily incident counts.
- **Restoration Performance:** Median and 90th percentile duration measures to capture typical and extreme performance.
- **Impact:** Total customers affected.

## Limitations
- **Synthetic Data:** The dataset is generated probabilistically and may not fully reflect real-world seasonality or complex asset behaviors.
- **Simplified Logic:** Weather impact is modeled as a random factor rather than correlated with actual meteorological data.
- **Categorical Depth:** Asset types and causes are simplified for demonstration purposes.

## Future Improvements
- **Integration with Real Data:** Connect to internal incident management systems.
- **Predictive Modeling:** Train ML models to predict restoration times based on initial incident reports.
- **Geospatial Analysis:** Map incidents to specific coordinates for heatmapping.
