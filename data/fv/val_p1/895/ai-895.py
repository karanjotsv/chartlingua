import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# The script expects a single command-line argument: the path to the JSON file.
if len(sys.argv) != 2:
    sys.exit(1)

# Use pathlib for robust path handling.
json_file_path = Path(sys.argv[1])

# Read data from the JSON file.
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract chart data, texts, and colors from the loaded JSON.
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for the pie chart trace.
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Initialize a Figure object.
fig = go.Figure()

# Add the pie chart trace.
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=2)
    ),
    texttemplate='%{value}%',
    textposition='inside',
    textfont=dict(size=14, color='white'),
    hoverinfo='label+percent',
    sort=False,  # This is crucial to preserve the original data order.
    domain=dict(x=[0, 0.75]) # Allocate space on the right for the legend.
))

# Update the layout of the figure.
title_text = texts.get('title', '')

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=20)
    ),
    font=dict(
        family="Arial"
    ),
    legend=dict(
        orientation="v",
        traceorder='normal', # Ensures legend items match the data order.
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=0.77
    ),
    margin=dict(l=20, r=20, t=80, b=20),
    showlegend=True
)

# Derive the output image filename from the input JSON filename.
output_image_path = json_file_path.with_suffix('.png')

# Write the figure to a high-resolution PNG image file.
fig.write_image(str(output_image_path), scale=2)