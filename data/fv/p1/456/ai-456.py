import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- Script setup and data loading ---
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

output_path = json_path.with_suffix('.png')

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (json.JSONDecodeError, IOError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# --- Extract data from JSON ---
chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = chart_data.get('labels', [])
values = chart_data.get('values', [])
title_text = texts.get('title', '')

# --- Chart creation ---
fig = go.Figure()

# Add the pie trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1)
    ),
    textinfo='percent',
    textposition='outside',
    sort=False,  # This is crucial to preserve the order from the JSON file
    direction='clockwise',
    hoverinfo='label+percent+value'
))

# --- Layout and styling ---
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=16)
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    legend=dict(
        x=0.75,
        y=0.7,
        bordercolor='black',
        borderwidth=1,
        traceorder='normal' # Ensures legend items match data order
    ),
    margin=dict(l=50, r=50, t=100, b=50), # Margins to prevent clipping
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=True
)

# --- Finalize trace appearance ---
fig.update_traces(
    textfont=dict(family="Arial", size=12, color='black')
)

# --- Output ---
try:
    fig.write_image(output_path, scale=2)
    print(f"Chart saved to {output_path}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)