import sys
import json
import plotly.graph_objects as go
import pathlib

# This script requires a single command-line argument: the path to the JSON data file.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
output_image_path = json_file_path.with_suffix('.png')

# Load data and texts from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Prepare data for Plotly
labels = [item.get("label", "") for item in chart_data]
values = [item.get("value", 0) for item in chart_data]

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    hole=0,
    textinfo='percent',
    textfont_size=14,
    insidetextorientation='radial',
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise'
))

# Combine title and subtitle if they exist
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Combine source and note for the annotation
source_text = ""
if texts.get("source"):
    source_text += texts.get("source")
if texts.get("note"):
    if source_text:
        source_text += "<br>"
    source_text += texts.get("note")

# Update layout for a clean, professional look
fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    title_font_family="Arial",
    font_family="Arial",
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="auto",
        y=1,
        xanchor="left",
        x=1.05,
        font=dict(
            family="Arial"
        )
    ),
    margin=dict(l=40, r=200, t=60, b=80),  # Adjust right margin for the legend
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            x=0,
            y=-0.15,
            xref="paper",
            yref="paper",
            xanchor="left",
            yanchor="bottom",
            align="left",
            font=dict(
                family="Arial",
                size=12
            )
        )
    ] if source_text else []
)

# Generate the output image file
fig.write_image(str(output_image_path), scale=2)

print(f"Chart saved to {output_image_path}")