import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Create subplots for the pie charts
fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

# Add traces for each pie chart
chart_details = chart_data['charts']
for i, chart in enumerate(chart_details):
    labels = [d['label'] for d in chart['data']]
    values = [d['value'] for d in chart['data']]
    colors = chart['colors']
    
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker_colors=colors,
        sort=False,
        direction='clockwise',
        hole=0.0
    ), row=1, col=i + 1)

# Update trace properties
# While the original chart uses black boxes for labels, this is a non-standard
# feature. White text on the colored slice is the closest robust representation.
fig.update_traces(
    textposition='inside',
    texttemplate='%{label}<br>%{value}%',
    textfont=dict(color='white', size=14, family='Arial'),
    hoverinfo='label+percent',
    marker=dict(line=dict(color='#FFFFFF', width=2))
)

# Prepare annotations for titles and footer text
annotations = []
title_x_positions = [0.22, 0.78]
annotation_x_positions = [0.22, 0.78]

for i, chart in enumerate(chart_details):
    # Chart titles
    annotations.append(dict(
        text=chart['title'],
        x=title_x_positions[i],
        y=1.0,
        xref='paper',
        yref='paper',
        xanchor='center',
        yanchor='bottom',
        showarrow=False,
        font=dict(size=20, family='Arial')
    ))
    # Bottom annotations
    annotations.append(dict(
        text=chart['annotation_text'],
        x=annotation_x_positions[i],
        y=-0.05,
        xref='paper',
        yref='paper',
        xanchor='center',
        yanchor='top',
        align='center',
        showarrow=False,
        font=dict(size=12, family='Arial')
    ))

# Source annotation
annotations.append(dict(
    text=chart_data['texts']['source'],
    x=0.98,
    y=-0.1,
    xref='paper',
    yref='paper',
    xanchor='right',
    yanchor='bottom',
    showarrow=False,
    font=dict(size=11, family='Arial', color='grey')
))

# Update layout
fig.update_layout(
    showlegend=False,
    paper_bgcolor='#EBEBEB',
    plot_bgcolor='#EBEBEB',
    font_family="Arial",
    margin=dict(t=80, b=120, l=20, r=20),
    annotations=annotations
)

# Determine output filename and save the image
base_filename, _ = os.path.splitext(os.path.basename(json_path))
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart image saved to {output_filename}")