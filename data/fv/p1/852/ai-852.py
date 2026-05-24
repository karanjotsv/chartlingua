import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read and parse the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for the pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    sort=False,
    direction='clockwise',
    hoverinfo='none'
)])

# Update trace properties
fig.update_traces(
    textposition='inside',
    textinfo='label',
    insidetextfont={'family': 'Arial', 'size': 14, 'color': 'black'},
    marker={'line': {'color': 'white', 'width': 2}}
)

# Combine title and subtitle
title_text = texts.get('title', '')
subtitle_text = texts.get('subtitle', '')
if subtitle_text:
    title_text += f"<br><span style='font-size: 16px; font-weight: normal;'>{subtitle_text}</span>"

# Update layout properties
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_y=0.95,
    title_font={'family': 'Arial', 'size': 28},
    font_family='Arial',
    showlegend=False,
    margin=dict(t=120, b=80, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.05,
            xanchor='center',
            yanchor='top',
            font={'family': 'Arial', 'size': 12}
        )
    ]
)

# Define output filename based on the input JSON filename
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")