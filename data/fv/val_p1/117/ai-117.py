import sys
import json
import os
import plotly.graph_objects as go

# This script generates a chart from a JSON file specified as a command-line argument.

# Check if the JSON file path is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly pie chart
labels = [item.get('category') for item in chart_data]
values = [item.get('value') for item in chart_data]
pulls = [item.get('pull', 0) for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    pull=pulls,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=2)
    ),
    texttemplate='%{label}<br>%{value}%',
    insidetextfont=dict(family="Arial", size=14, color='black'),
    hoverinfo='label+percent',
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise',
    rotation=75
)

# Create the figure object
fig = go.Figure(data=[pie_trace])

# Update the layout of the chart
fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    title_font=dict(family="Arial", size=24, color='black'),
    font=dict(family="Arial", size=12, color='black'),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=100, b=30, l=30, r=30)
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(json_path)[0]
output_filename = f"{base_filename}.png"

# Write the figure to a high-resolution PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved to {output_filename}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)