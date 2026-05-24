import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Load the data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data lists for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the line trace
fig.add_trace(go.Scatter(
    x=categories,
    y=values,
    mode='lines+markers',
    line=dict(
        color=colors[0],
        width=2,
        shape='spline' # Creates a smoothed line (Bézier-like)
    ),
    marker=dict(
        color=colors[0],
        size=4
    ),
    showlegend=False
))

# --- Update Layout ---
fig.update_layout(
    font=dict(
        family="Arial",
        color="white"
    ),
    plot_bgcolor='black',
    paper_bgcolor='black',
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(color='white')
    ),
    yaxis=dict(
        type='log', # Set logarithmic scale
        showgrid=False,
        zeroline=False,
        tickfont=dict(color='white')
    ),
    margin=dict(l=60, r=40, t=40, b=40),
    height=500,
    width=800
)

# --- Title and Source (if they exist in JSON) ---
# This chart has no visible titles, so this logic will not execute
# but is included for robustness with other JSON files.
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
source_text = texts.get('source')

full_title = ""
if title_text:
    full_title += f"<span style='font-size: 20px;'><b>{title_text}</b></span>"
if subtitle_text:
    full_title += f"<br><span style='font-size: 14px;'>{subtitle_text}</span>"

if full_title:
    fig.update_layout(
        title=dict(
            text=full_title,
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top'
        )
    )

if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0, y=-0.15,
        xanchor='left', yanchor='top',
        showarrow=False,
        font=dict(size=12)
    )

# Define the output image path from the input JSON path
output_image_path = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")