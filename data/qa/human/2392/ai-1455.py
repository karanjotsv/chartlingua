import sys
import json
import plotly.graph_objects as go
import pathlib

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_filepath = sys.argv[1]

# Load chart data from the specified JSON file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_filepath}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_filepath}'")
    sys.exit(1)

# Extract data and text from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

labels = [item.get('label') for item in chart_data]
values = [item.get('value') for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    texttemplate='%{label} %{value}%',
    textposition='outside',
    sort=False,
    direction='clockwise',
    rotation=310 # Adjust rotation to approximate the visual layout
))

# Combine title and subtitle
title_parts = [texts.get('title'), texts.get('subtitle')]
full_title = "<br>".join(filter(None, title_parts))

# Combine source and note for the annotation
source_parts = [texts.get('source'), texts.get('note')]
full_source_text = "<br>".join(filter(None, source_parts))

annotations = []
if full_source_text:
    annotations.append(
        dict(
            text=full_source_text,
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=0,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    )

# Update layout for a clean, professional look
fig.update_layout(
    title_text=full_title,
    title_x=0.5,
    font=dict(family="Arial", size=14),
    showlegend=False,
    margin=dict(t=60, b=60, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=annotations
)

# Determine the output filename from the input JSON path
base_name = pathlib.Path(json_filepath).stem
output_filename = f"{base_name}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")