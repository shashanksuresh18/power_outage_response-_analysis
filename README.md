# Outage Response Analysis

An analytics and DevOps-focused project for analyzing power outage response performance.

## Overview
This project processes synthetic outage data to compute key operational metrics and visualizes them in an interactive dashboard. It demonstrates a production-ready pipeline with automated testing and CI/CD integration.

## Features
- **Data Pipeline**: Generates, cleans, and features-engineers synthetic outage data.
- **Metrics Engine**: Computes volume, impact, and response performance metrics (Median, P90).
- **Dashboard**: Interactive Plotly Dash application for data exploration.
- **CI/CD**: GitHub Actions workflow for automated testing and validation.

## Repository Structure
```
outage-response-analysis/
├── data/               # Raw and processed data
├── notebooks/          # EDA notebooks
├── src/
│   ├── data/           # Data processing scripts
│   ├── metrics/        # Metric computation
│   └── viz/            # Dashboard code
├── tests/              # Unit tests
├── .github/workflows/  # CI/CD configuration
└── README.md
```

## Setup
1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd outage-response-analysis
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run the Data Pipeline
Execute the following to generate and process fresh data:
```bash
python src/data/generate.py
python src/data/clean.py
python src/data/features.py
python src/metrics/compute.py
```

### Run the Dashboard
Launch the dashboard locally:
```bash
python src/viz/dashboard.py
```
Access it at http://127.0.0.1:8050/

### Run Tests
Execute the test suite:
```bash
pytest
```

## Documentation
See [REPORT.md](REPORT.md) for analysis insights and limitations.
