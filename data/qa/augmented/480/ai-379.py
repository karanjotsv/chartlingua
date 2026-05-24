import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data, texts, and colors from the JSON object
chart_data = chart_config.get("chart_data", [])
texts = chart_config.get("texts", {})
colors = chart_config.get("colors", [])

# Prepare data for Plotly
# The data is extracted top-to-bottom, so we reverse it for Plotly's bottom-to-top rendering
categories = [item['category'] for item in chart_data][::-1]
values = [item['value'] for item in chart_data][::-1]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=[f"{v}%" for v in values],
    textposition='outside',
    cliponaxis=False  # Prevents text labels from being clipped
))

# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title=texts.get('x_axis_title', ''),
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        zeroline=False,
        ticksuffix='%',
        range=[0, max(values) * 1.15] # Ensure space for labels
    ),
    yaxis=dict(
        title=texts.get('y_axis_title', ''),
        showgrid=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=120, r=40, t=50, b=80),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.1,
            xanchor='right',
            yanchor='top',
            align='right'
        )
    ]
)

# Define the output filename based on the input JSON filename
output_filename = json_file_path.with_suffix('.png')

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")