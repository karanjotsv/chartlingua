import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- Script Execution ---
# Ensure a single command-line argument is provided
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the provided path is a valid file
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_file_path}'")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add data traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines+markers',
        line=dict(color=colors[i % len(colors)]),
        marker=dict(
            symbol='diamond',
            color=colors[i % len(colors)],
            size=6
        )
    ))

# Build combined title string using HTML for line breaks
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Configure the layout of the chart
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickangle=-45,
        automargin=True,
        showgrid=True,
        gridcolor='#CCCCCC'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 18],
        dtick=2,
        automargin=True,
        showgrid=True,
        gridcolor='#CCCCCC'
    ),
    legend=dict(
        yanchor="top",
        y=0.98,
        xanchor="right",
        x=0.98
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=80, b=150)
)

# Define the output image filename based on the input JSON filename
output_filename = json_file_path.with_suffix('.png').name

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")