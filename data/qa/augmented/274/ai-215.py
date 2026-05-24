import sys
import json
import plotly.graph_objects as go
import os

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read the JSON data file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly traces
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the bar trace with data labels
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False,  # Prevents data labels from being clipped
    textfont=dict(family="Arial", size=12, color='black')
))

# Combine title and subtitle if they exist
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

# Configure the layout of the chart
fig.update_layout(
    font=dict(family="Arial"),
    title=dict(text=full_title, x=0.05, xanchor='left'),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 350],
        showgrid=True,
        gridcolor='lightgray',
        zeroline=True,
        zerolinecolor='lightgray'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=50, r=40, b=100, l=80)
)

# Add source annotation
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=1, y=-0.18,
        xanchor='right', yanchor='top',
        showarrow=False,
        font=dict(family="Arial", size=12, color='#555555')
    )

# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the chart to a PNG file and print a confirmation message
fig.write_image(output_filename, scale=2)
print(f"Chart successfully generated and saved to {output_filename}")