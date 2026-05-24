import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

labels = [item['category'].replace('<br>', ' ') for item in chart_data]
values = [item['value'] for item in chart_data]

# Format text for display inside slices, combining category and value
text_inside_slices = [f"{item['category']}<br>{item['value']}%" for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    hole=0.4,
    text=text_inside_slices,
    textposition='inside',
    insidetextorientation='radial',
    insidetextfont=dict(
        family='Arial',
        size=12,
        color=colors['text']
    ),
    marker=dict(
        colors=colors['slices'] * len(labels),  # Use the same color for all slices
        line=dict(color=colors['lines'], width=1.5)
    ),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=150  # Adjusts start position to match original layout
)

# Combine title and subtitle
title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

# Create the layout
layout = go.Layout(
    title_text=title_text,
    title_x=0.05,
    title_y=0.92,
    font=dict(
        family="Arial",
        size=14,
        color=colors['text']
    ),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=120, b=40, l=40, r=40)
)

# Create the figure and add the trace
fig = go.Figure(data=[pie_trace], layout=layout)

# Determine output filename from input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")