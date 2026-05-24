import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON data from the file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_json = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON.")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_json.get('chart_data', [])
texts = chart_json.get('texts', {})
colors = chart_json.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#2E6494',
    text=[f"{v}%" for v in values],
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=16,
        color='black'
    ),
    hoverinfo='none'
))

# Update layout
title_text = f"<b>{texts.get('title', '')}</b>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.02,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(
            family="Arial",
            size=24,
            color='black'
        )
    ),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(
            family="Arial",
            size=16,
            color='black'
        )
    ),
    yaxis=dict(
        visible=False,
        range=[0, max(values) * 1.2]  # Add padding for text labels
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=40, r=40, t=100, b=80)
)

# Determine the output filename from the input JSON path
base_filename = Path(json_path).stem
output_filename = f"{base_filename}.png"

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")