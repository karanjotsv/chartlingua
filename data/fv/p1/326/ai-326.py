import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and settings from the JSON structure
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', {})

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors.get('bar_colors'),
    marker_line_color=colors.get('bar_border_color'),
    marker_line_width=1,
    showlegend=False
))

# Combine title and subtitle if they exist
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font=dict(
        family="Arial",
        color=colors.get('font_color', '#000000')
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickangle=-90,
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 600],
        tickvals=[0, 100, 200, 300, 400, 500, 600],
        showgrid=True,
        gridcolor=colors.get('grid_color')
    ),
    plot_bgcolor=colors.get('plot_bgcolor'),
    paper_bgcolor=colors.get('paper_bgcolor'),
    bargap=0.15,
    margin=dict(l=50, r=20, t=30, b=150)
)

# Define the output filename based on the input JSON filename
output_filename = json_file_path.with_suffix(".png")

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")