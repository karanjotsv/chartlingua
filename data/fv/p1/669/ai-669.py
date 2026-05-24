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

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data from the JSON object
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Create the figure
fig = go.Figure()

# Add traces for each density plot
for i, series in enumerate(data_series):
    hex_color = colors[i % len(colors)]
    # Convert hex to rgba for fill transparency
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    fill_color_rgba = f'rgba({r}, {g}, {b}, 0.7)'

    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color='black', width=1.5),
        fill='tozeroy',
        fillcolor=fill_color_rgba,
        line_shape='spline', # To create smooth curves from the data points
        hoverinfo='skip'
    ))

# Combine title and subtitle
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Configure the layout
fig.update_layout(
    template="ggplot2",
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_label'),
        range=[0, 5.2],
        tickvals=[0, 1, 2, 3, 4, 5],
        gridcolor='white',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_label'),
        range=[-0.02, 1.05],
        tickvals=[0.0, 0.3, 0.6, 0.9],
        gridcolor='white',
        zeroline=False
    ),
    legend=dict(
        title_text=texts.get('legend_title'),
        itemsizing='constant'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=60, r=30, t=50, b=60),
    plot_bgcolor='#EFEFEF',
    paper_bgcolor='white'
)

# Determine the output image filename from the input JSON filename
output_image_path = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(str(output_image_path), scale=2)

print(f"Chart saved to {output_image_path}")