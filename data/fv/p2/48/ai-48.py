import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for the required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Use pathlib for robust path handling
json_path = Path(sys.argv[1])

# Verify the input file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read and parse the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series from the JSON
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series.get('name'),
        x=series.get('x'),
        y=series.get('y'),
        orientation='h',
        marker_color=colors[i % len(colors)] if colors else None
    ))

# Build the title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text = f"<b>{title_text}</b><br><sub>{texts.get('subtitle')}</sub>"

# Update layout for a professional appearance
fig.update_layout(
    barmode='group',
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        showline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        autorange='reversed',  # Ensure categories appear in the order provided (top to bottom)
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
        title_text=texts.get('legend_title')
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=250, r=40, t=80, b=80) # Increased left margin for long labels
)

# Determine the output filename and save the image
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")