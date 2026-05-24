import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data and texts from the loaded JSON
data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Create a figure
fig = go.Figure()

# Define line widths
line_widths = [2, 1.5, 1.5] 

# Add traces for each data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        name=series['name'],
        line=dict(color=colors[i], width=line_widths[i]),
        connectgaps=False  # Do not connect across null values (WWII gap)
    ))

# Build the title string
title_text = ""
if texts.get("title"):
    title_text += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    title_text += f'<br>{texts["subtitle"]}'

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        xanchor='left',
        y=0.98,
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    xaxis=dict(
        tickmode='linear',
        tick0=1930,
        dtick=4,
        showgrid=False,
        zeroline=False,
        ticks='outside',
        tickson='boundaries',
        showline=True,
        linecolor='lightgrey'
    ),
    yaxis=dict(
        autorange='reversed',
        range=[85, -5],
        tickmode='linear',
        tick0=0,
        dtick=10,
        gridcolor='lightgrey',
        zeroline=False,
        showline=True,
        linecolor='lightgrey'
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=40, r=40, t=60, b=40)
)

# Determine output filename from the input JSON filename
output_filename = f"{json_file_path.stem}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")