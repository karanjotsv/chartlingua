import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = Path(sys.argv[1])

# Verify the file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and text for plotting
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        mode='lines+markers',
        line=dict(color=colors[i] if i < len(colors) else None),
        marker=dict(
            color=colors[i] if i < len(colors) else None,
            symbol='diamond',
            size=8
        )
    ))

# Build the title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout
fig.update_layout(
    title=dict(
        text=f"<b>{title_text}</b>",
        x=0.5,
        font=dict(size=20)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        range=[0, 3.5],
        tick0=0,
        dtick=0.5,
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 4.5],
        tick0=0,
        dtick=0.5,
        gridcolor='lightgrey'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='#F0F0F0',
    margin=dict(l=80, r=40, t=90, b=80)
)

# Define output filename from the input JSON file's base name
output_filename = f"{json_file_path.stem}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")