import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('name', ''),
        line=dict(color=colors[i] if i < len(colors) else '#000000', width=2),
        hoverinfo='none'
    ))

# Combine title and subtitle if they exist
title_text = texts.get('title', '')
subtitle_text = texts.get('subtitle', '')
if title_text and subtitle_text:
    full_title = f"{title_text}<br><sub>{subtitle_text}</sub>"
elif title_text:
    full_title = title_text
else:
    full_title = None

# Update layout
fig.update_layout(
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=14
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=80, b=80),
    xaxis=dict(
        range=[0, 5.5],
        tickvals=[0, 1, 2, 3, 4, 5],
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True,
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        range=[0, 5.5],
        tickvals=[0, 1, 2, 3, 4, 5],
        showline=True,
        linewidth=1.5,
        linecolor='black',
        mirror=True,
        showgrid=False,
        zeroline=False
    )
)

# Add annotations from JSON
annotations_data = texts.get('annotations', [])
for ann in annotations_data:
    fig.add_annotation(
        x=ann.get('x'),
        y=ann.get('y'),
        text=ann.get('text'),
        showarrow=False,
        font=dict(
            family="Arial",
            size=14
        ),
        xanchor='left',
        yanchor='bottom'
    )
    
# Derive output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")