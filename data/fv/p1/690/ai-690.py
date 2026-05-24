import sys
import json
import plotly.graph_objects as go
import pathlib

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data and settings from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Initialize figure
fig = go.Figure()

# Add data series from JSON
for i, series in enumerate(chart_data.get('chart_data', [])):
    color = chart_data.get('colors', [])[i % len(chart_data.get('colors', ['#000000']))]
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode=series.get('mode', 'lines'),
        name=series.get('name', ''),
        line=dict(color=color, width=2),
        marker=dict(
            color=color,
            symbol=series.get('marker', {}).get('symbol'),
            size=series.get('marker', {}).get('size'),
            line=series.get('marker', {}).get('line')
        ) if 'marker' in series else None,
        showlegend=False
    ))

# Extract text elements
texts = chart_data.get('texts', {})
title_text = texts.get('title')
x_axis_title = texts.get('x_axis_title')
y_axis_title = texts.get('y_axis_title')
annotations_data = texts.get('annotations', [])

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(text=title_text) if title_text else None,
    xaxis=dict(
        title=x_axis_title,
        range=[0, 90],
        dtick=10,
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True,
        showgrid=False,
        ticks='outside'
    ),
    yaxis=dict(
        title=dict(text=y_axis_title, standoff=10),
        range=[0, 5.1],
        dtick=1,
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True,
        showgrid=False,
        ticks='outside'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=20, t=40, b=50),
    showlegend=False,
    shapes=chart_data.get('shapes', [])
)

# Add annotations
for ann in annotations_data:
    fig.add_annotation(ann)

# Generate output filename from JSON path
output_filename = pathlib.Path(json_path).stem + ".png"

# Write image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")