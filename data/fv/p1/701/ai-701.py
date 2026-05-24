import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [item['text_label'] for item in chart_data]

# The top-most bar has its label outside, the rest are inside
text_positions = ['inside'] * (len(chart_data) - 1) + ['outside']

# Create the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(
        color=colors[0] if colors else '#2b7bba',
        line=dict(width=0)
    ),
    text=text_labels,
    textposition=text_positions,
    textfont=dict(
        family="Arial",
        size=10,
        color="#333333"
    ),
    insidetextanchor='end',
    hoverinfo='none'
))

# Update layout
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

max_value = max(values) if values else 0

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        font=dict(size=16, family="Arial", color='black')
    ),
    xaxis=dict(
        title=texts.get('x_axis_title', ''),
        showgrid=True,
        gridcolor='#d3d3d3',
        gridwidth=1,
        zeroline=False,
        showline=False,
        showticklabels=True,
        tickformat='s',
        range=[0, max_value * 1.1] # Add padding for the outside label
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=True,
        autorange=True # Data order in JSON determines display order
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='#f0f0f0',
    paper_bgcolor='#f0f0f0',
    margin=dict(l=300, r=20, t=80, b=50), # Increased left margin for long labels
    bargap=0.3
)

# Determine output filename from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")