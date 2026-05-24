import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
categories = chart_data.get('categories', [])
series_data = chart_data.get('series', [])

# Initialize the figure
fig = go.Figure()

# Add traces for each data series, iterating to preserve order
for i, series in enumerate(series_data):
    fig.add_trace(go.Scatter(
        x=categories,
        y=series.get('y', []),
        name=series.get('name', ''),
        mode='lines',
        line=dict(color=colors[i % len(colors)]) # Use modulo to prevent index errors
    ))

# Build the title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=18)
    ),
    xaxis=dict(
        title=texts.get('x_axis_title', ''),
        tickmode='array',
        tickvals=categories,
        ticktext=categories,
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False
    ),
    yaxis=dict(
        title=texts.get('y_axis_title', ''),
        range=[34.0, 37.4],
        dtick=0.2,
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(t=80, b=100, l=80, r=40),
    width=1000,
    height=600
)

# Derive output filename from the input JSON path
output_filename = pathlib.Path(json_path).stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")