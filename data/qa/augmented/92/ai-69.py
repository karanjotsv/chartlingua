import sys
import json
import os
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)

# Extract data for the chart
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=1)),
    textinfo='label+percent',
    textposition='outside',
    insidetextorientation='radial',
    sort=False,  # Preserve the order from the JSON file
    pull=[0.01] * len(labels) # Slight pull for better visual separation
)])

# Combine title and subtitle
title_text = texts.get('title') or ''
subtitle_text = texts.get('subtitle') or ''
if subtitle_text:
    title_text = f"{title_text}<br><sub>{subtitle_text}</sub>"

# Update layout
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    showlegend=False,
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    margin=dict(t=60, b=60, l=80, r=80),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Add source annotation
fig.add_annotation(
    text=texts.get('source', ''),
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0.99,
    y=-0.01,
    xanchor='right',
    yanchor='top',
    font=dict(size=12, color='grey')
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_filename = f"{base_filename}.png"

# Save the chart as a PNG image
fig.write_image(output_image_filename, scale=2)

print(f"Chart saved as {output_image_filename}")