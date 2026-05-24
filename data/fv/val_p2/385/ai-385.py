import sys
import json
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the sole command-line argument.
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
categories = data.get('categories', [])
series = data.get('series', [])

# --- 2. Create the Plotly Figure ---
fig = go.Figure()

# Add traces in the order they appear in the JSON (bottom-to-top stacking)
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        name=s.get('name', ''),
        x=categories,
        y=s.get('values', []),
        marker_color=colors[i % len(colors)]
    ))

# --- 3. Configure Layout and Styling ---
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text = f"<b>{title_text}</b><br>{texts.get('subtitle')}"

fig.update_layout(
    barmode='stack',
    title={
        'text': title_text,
        'x': 0.05,
        'xanchor': 'left',
        'y': 0.95,
        'yanchor': 'top'
    },
    xaxis={
        'title_text': texts.get('x_axis_title'),
        'tickangle': -90,
        'categoryorder': 'array',
        'categoryarray': categories
    },
    yaxis={
        'title_text': texts.get('y_axis_title'),
        'range': [0, 160],
        'gridcolor': '#e0e0e0'
    },
    legend={
        'traceorder': 'reversed', # Reverses legend items to match original image
        'x': 0.99,
        'y': 0.99,
        'xanchor': 'right',
        'yanchor': 'top'
    },
    font={
        'family': "Arial",
        'size': 12
    },
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=80, b=150),
    showlegend=True
)

# --- 4. Output the Image ---
# Derive the output filename from the input JSON path
base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as '{output_filename}'")