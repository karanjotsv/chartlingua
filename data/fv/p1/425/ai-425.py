import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts from the JSON structure
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]
bar_color = colors[0] if colors else '#375A9E'

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=bar_color,
    text=values,
    textposition='inside',
    textangle=-90,
    insidetextanchor='middle',
    insidetextfont=dict(family="Arial", size=12, color="white"),
    texttemplate='%{text}',
    hoverinfo='none',
    showlegend=False
))

# Combine title and subtitle if available
title_text = texts.get('title') or ''

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(
            family="Arial",
            size=24
        )
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        zeroline=False,
        tickfont=dict(family="Arial")
    ),
    yaxis=dict(
        visible=False
    ),
    plot_bgcolor='#EAEAEA',
    paper_bgcolor='white',
    font=dict(family="Arial"),
    margin=dict(t=80, b=50, l=50, r=50),
    bargap=0.2
)

# Define output filename based on the input JSON filename
output_filename = json_file_path.stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")