import nbformat as nbf
import os

def create_eda_notebook(output_path):
    nb = nbf.v4.new_notebook()
    
    nb['cells'] = [
        nbf.v4.new_markdown_cell("# Exploratory Data Analysis: Outage Response\n\nThis notebook analyzes the cleaned outage data to identify patterns and performance metrics."),
        nbf.v4.new_code_cell("import pandas as pd\nimport plotly.express as px\nimport plotly.io as pio\npio.renderers.default = 'notebook'"),
        nbf.v4.new_markdown_cell("## 1. Load Data"),
        nbf.v4.new_code_cell("df = pd.read_parquet('../data/processed/eda_outages.parquet')\ndf.head()"),
        nbf.v4.new_markdown_cell("## 2. Overview Statistics"),
        nbf.v4.new_code_cell("df.info()\ndf.describe()"),
        nbf.v4.new_markdown_cell("## 3. Incident Volume\n\nAnalyze the number of incidents over time."),
        nbf.v4.new_code_cell("daily_counts = df.groupby(df['reported_at'].dt.date).size()\nfig = px.line(daily_counts, title='Daily Incident Volume')\nfig.show()"),
        nbf.v4.new_markdown_cell("## 4. Response Performance\n\nAnalyze restoration times by cause and asset type."),
        nbf.v4.new_code_cell("fig = px.box(df, x='cause', y='duration_minutes', title='Duration Distribution by Cause')\nfig.show()"),
        nbf.v4.new_code_cell("fig = px.box(df, x='asset_type', y='duration_minutes', title='Duration Distribution by Asset Type')\nfig.show()"),
        nbf.v4.new_markdown_cell("## 5. Impact Analysis\n\nAnalyze customers affected."),
        nbf.v4.new_code_cell("fig = px.histogram(df, x='customers_affected', title='Distribution of Customers Affected')\nfig.show()")
    ]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        nbf.write(nb, f)
    
    print(f"Created notebook at {output_path}")

if __name__ == "__main__":
    create_eda_notebook("notebooks/01_eda.ipynb")
