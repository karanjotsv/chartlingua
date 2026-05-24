import sys
import json
import plotly.graph_objects as go
import pathlib

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument.
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists.
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Read and parse the JSON file.
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_file_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure.
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly by extracting labels and values while preserving order.
labels = [item.get('label') for item in chart_data]
values = [item.get('value') for item in chart_data]

# Initialize a Plotly figure.
fig = go.Figure()

# Add the pie chart trace.
# 'sort=False' is crucial to maintain the original order from the JSON data.
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=1.5)),
    sort=False,
    direction='counterclockwise',
    textinfo='none',  # No text labels on the pie slices themselves.
    hoverinfo='label+percent'
))

# Update the figure's layout.
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sup>{texts.get('subtitle')}</sup>"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_y=0.95,
    title_font_size=20,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=40, r=40, t=100, b=80),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output image filename from the input JSON filename.
output_image_path = json_file_path.with_suffix('.png')

# Save the figure as a high-resolution PNG image.
fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to '{output_image_path}'")