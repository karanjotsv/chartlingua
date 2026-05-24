import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- 2. Extract data for Plotly ---
data = chart_data.get("chart_data", [])
texts = chart_data.get("texts", {})
colors = chart_data.get("colors", [])

labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add Pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors),
    hole=0,
    sort=False,
    direction='clockwise',
    textinfo='percent+label',
    texttemplate='%{label} %{value}%',
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=14
    ),
    hoverinfo='label+percent',
    automargin=True
))

# --- 4. Configure layout ---
title_text = texts.get('title')
source_text = texts.get('source')

annotations = []
if source_text:
    annotations.append(
        dict(
            text=source_text,
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=0,
            xanchor='right',
            yanchor='bottom',
            font=dict(family='Arial', size=12, color='#808080')
        )
    )

fig.update_layout(
    title_text=title_text,
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(l=80, r=80, t=50, b=80),
    plot_bgcolor='white',
    paper_bgcolor='white',
    annotations=annotations
)

# --- 5. Save the figure as a PNG image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")