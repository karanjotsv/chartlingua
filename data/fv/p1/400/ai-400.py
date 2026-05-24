import sys
import json
import plotly.graph_objects as go
import os

# Data Source: BBC analysis of UNFCCC data from 2018.
# Original Source Document Reference: https://unfccc.int/documents/223579

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0,
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=1) # Add a thin white line between slices
    ),
    sort=False,  # This is crucial to preserve the order from the JSON
    direction='clockwise',
    rotation=90,  # Starts the first slice at the 12 o'clock position
    textinfo='label',
    textposition='outside',
    automargin=True
))

# Update layout
title_text = texts.get('title', '')

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=16
    ),
    showlegend=False,
    margin=dict(t=80, b=40, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Generate output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)