import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import os

# Initialize App
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# Load Data
DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/processed/eda_outages.parquet')

def load_data():
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()
    return pd.read_parquet(DATA_PATH)

df = load_data()

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Outage Response Dashboard", className="text-center text-primary mb-4"), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Label("Date Range"),
            dcc.DatePickerRange(
                id='date-picker',
                start_date=df['reported_at'].min().date() if not df.empty else None,
                end_date=df['reported_at'].max().date() if not df.empty else None,
                display_format='YYYY-MM-DD'
            )
        ], width=4),
        dbc.Col([
            html.Label("Region"),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': r, 'value': r} for r in df['region'].unique()] if not df.empty else [],
                multi=True,
                placeholder="Select Region"
            )
        ], width=4),
        dbc.Col([
            html.Label("Cause"),
            dcc.Dropdown(
                id='cause-dropdown',
                options=[{'label': c, 'value': c} for c in df['cause'].unique()] if not df.empty else [],
                multi=True,
                placeholder="Select Cause"
            )
        ], width=4),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Total Incidents", className="card-title"),
                html.H2(id='kpi-incidents', className="card-text")
            ])
        ], color="light"), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Customers Affected", className="card-title"),
                html.H2(id='kpi-customers', className="card-text")
            ])
        ], color="light"), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Median Restoration", className="card-title"),
                html.H2(id='kpi-restoration', className="card-text")
            ])
        ], color="light"), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("P90 Restoration", className="card-title"),
                html.H2(id='kpi-p90', className="card-text")
            ])
        ], color="light"), width=3),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='incidents-over-time'), width=8),
        dbc.Col(dcc.Graph(id='incidents-by-cause'), width=4),
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='restoration-distribution'), width=6),
        dbc.Col(dcc.Graph(id='customers-impact'), width=6),
    ])
], fluid=True)

# Callbacks
@callback(
    [Output('kpi-incidents', 'children'),
     Output('kpi-customers', 'children'),
     Output('kpi-restoration', 'children'),
     Output('kpi-p90', 'children'),
     Output('incidents-over-time', 'figure'),
     Output('incidents-by-cause', 'figure'),
     Output('restoration-distribution', 'figure'),
     Output('customers-impact', 'figure')],
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('region-dropdown', 'value'),
     Input('cause-dropdown', 'value')]
)
def update_dashboard(start_date, end_date, regions, causes):
    if df.empty:
        return "0", "0", "0 min", "0 min", {}, {}, {}, {}
    
    # Filter Data
    dff = df.copy()
    if start_date:
        dff = dff[dff['reported_at'] >= pd.to_datetime(start_date)]
    if end_date:
        dff = dff[dff['reported_at'] <= pd.to_datetime(end_date)]
        
    if regions:
        dff = dff[dff['region'].isin(regions)]
    if causes:
        dff = dff[dff['cause'].isin(causes)]
        
    if dff.empty:
         return "0", "0", "0 min", "0 min", {}, {}, {}, {}
        
    # KPIs
    kpi_vol = f"{len(dff):,}"
    kpi_cust = f"{dff['customers_affected'].sum():,}"
    kpi_rest = f"{dff['duration_minutes'].median():.0f} min"
    kpi_p90 = f"{dff['duration_minutes'].quantile(0.90):.0f} min"
    
    # Charts
    # 1. Incidents Over Time
    counts = dff.groupby(dff['reported_at'].dt.date).size().reset_index(name='count')
    fig_time = px.line(counts, x='reported_at', y='count', title="Daily Incident Volume", template='plotly_white')
    
    # 2. Incidents by Cause
    fig_cause = px.pie(dff, names='cause', title="Incidents by Cause", hole=0.4)
    
    # 3. Restoration Distribution
    fig_hist = px.histogram(dff, x='duration_minutes', nbins=50, title="Restoration Time Distribution", 
                            color='cause', marginal='box', template='plotly_white')
    
    # 4. Impact vs Duration
    fig_scatter = px.scatter(dff, x='duration_minutes', y='customers_affected', color='priority',
                             title="Impact vs Duration", opacity=0.6, template='plotly_white')
    
    return kpi_vol, kpi_cust, kpi_rest, kpi_p90, fig_time, fig_cause, fig_hist, fig_scatter

if __name__ == '__main__':
    app.run(debug=True)
