import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Read the JSON file
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and text from the loaded JSON
chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
categories = chart_data.get('categories', [])
series = chart_data.get('series', [])

# --- 2. Create the Chart ---
# Initialize the figure
fig = go.Figure()

# Add a trace for each data series
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s.get('values', []),
        name=s.get('name', ''),
        marker_color=colors[i % len(colors)]
    ))

# --- 3. Configure Layout ---
# Combine title and subtitle if available
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    barmode='group',
    xaxis={
        'title_text': texts.get('x_axis_title'),
        'tickfont': {'size': 12},
        'showgrid': False,
        'zeroline': False
    },
    yaxis={
        'title_text': texts.get('y_axis_title'),
        'range': [0, 200],
        'tickmode': 'linear',
        'dtick': 20,
        'gridcolor': '#E0E0E0',
        'zerolinecolor': '#E0E0E0'
    },
    legend={
        'orientation': 'h',
        'yanchor': 'top',
        'y': -0.15,
        'xanchor': 'center',
        'x': 0.5
    },
    plot_bgcolor='white',
    paper_bgcolor='white',
    font={
        'family': 'Arial',
        'size': 14,
        'color': 'black'
    },
    margin=dict(l=50, r=30, t=80, b=120)
)

# --- 4. Output the Image ---
# Derive output filename from the input JSON filename
output_filename = f"{json_path.stem}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")