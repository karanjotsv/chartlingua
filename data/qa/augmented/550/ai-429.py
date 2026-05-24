import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{text:.2f}',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Build title and source annotations
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

annotations = []
source_text = texts.get('source')
if source_text:
    annotations.append(
        dict(
            text=source_text,
            xref="paper", yref="paper",
            x=1.0, y=-0.15,
            xanchor='right', yanchor='top',
            showarrow=False,
            font=dict(family="Arial", size=10, color="grey")
        )
    )

# Update layout for a clean, professional look
fig.update_layout(
    title_text=full_title,
    title_x=0.05,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[0, 12.5],
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        zeroline=False
    ),
    yaxis=dict(
        autorange="reversed",
        showgrid=False,
        zeroline=False
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=120, r=50, t=50, b=80),
    annotations=annotations
)

# Determine output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")