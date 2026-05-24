import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and text from the JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    name=''
))

# Build the title string using HTML for formatting
title_text = ""
if texts.get("title"):
    title_text += f"<b style='font-size: 32px;'>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><i style='font-size: 16px;'>{texts['subtitle']}</i>"


# Update layout
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_font_family="Arial",
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=categories,
        ticktext=categories,
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 40000000],
        dtick=10000000,
        gridcolor='#D3D3D3',
        gridwidth=1
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=100, b=80)
)

# Define output filename from the input JSON filename
output_path = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")