import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get('chart_data', {})
categories = chart_data.get('categories', [])
series = chart_data.get('series', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Create a figure
fig = go.Figure()

# Add a trace for each data series
for i, s in enumerate(series):
    fig.add_trace(go.Scatter(
        x=categories,
        y=s.get('y', []),
        name=s.get('name', ''),
        mode='lines',
        line=dict(color=colors[i % len(colors)])
    ))

# Build the title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=True,
        gridcolor='lightgray',
        tickmode='array',
        tickvals=categories,
        ticktext=[str(c) for c in categories]
    ),
    yaxis=dict(
        range=[0, 250],
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=True,
        gridcolor='lightgray'
    ),
    plot_bgcolor='white',
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.98,
        xanchor="left",
        x=1.01
    ),
    margin=dict(l=60, r=150, t=80, b=50)
)

# Add source annotation if it exists
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0, y=-0.15,
        showarrow=False,
        align="left",
        xanchor='left',
        font=dict(size=10, color="gray")
    )

# Define output image path from the JSON filename
output_image_path = json_file_path.with_suffix('.png')

# Save the figure to a file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")