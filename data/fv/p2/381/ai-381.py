import sys
import json
import plotly.graph_objects as go
import os

# This script requires one command-line argument: the path to the JSON configuration file.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load chart configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = config.get('chart_data', [])
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
annotations = [item['annotation_text'] for item in chart_data]

# Extract text elements
texts = config.get('texts', {})
title_text = texts.get('title', '')
subtitle_text = texts.get('subtitle', '')
x_axis_title = texts.get('x_axis_title', '')
y_axis_title = texts.get('y_axis_title', '')

# Extract colors
colors = config.get('colors', [])
bar_color = colors[0] if colors else '#1f9a5f'

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=bar_color,
    text=annotations,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=10,
        color='black'
    )
))

# Combine title and subtitle using HTML for multi-line support
full_title = f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><span style='font-size: 14px;'>{subtitle_text}</span>"

# Update layout for a professional appearance
fig.update_layout(
    title=dict(
        text=full_title,
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),
    xaxis_title=x_axis_title,
    yaxis_title=y_axis_title,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        range=[0, 25000000],
        dtick=5000000
    ),
    xaxis=dict(
        showgrid=False
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(t=100, b=80, l=80, r=40)
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")