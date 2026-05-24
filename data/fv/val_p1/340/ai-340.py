import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- Argument and File Handling ---
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <path_to_json_file>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

base_filename = json_file_path.stem

# --- Data Loading ---
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# --- Data Preparation ---
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# --- Chart Creation ---
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else '#A42222',
    name=''
))

# --- Layout and Styling ---
title_text = f"<b>{texts.get('title', '')}</b>"

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 28}
    },
    xaxis={
        'title_text': texts.get('x_axis_title'),
        'type': 'category',
        'tickangle': -90,
        'showline': True,
        'linewidth': 1,
        'linecolor': 'black'
    },
    yaxis={
        'title_text': texts.get('y_axis_title'),
        'range': [0, 20000000],
        'tickformat': ',',
        'dtick': 5000000,
        'showgrid': True,
        'gridcolor': '#E0E0E0',
        'gridwidth': 1,
        'showline': True,
        'linewidth': 1,
        'linecolor': 'black'
    },
    font=dict(family="Arial", size=14, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=100, b=80)
)

# --- Output Generation ---
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")