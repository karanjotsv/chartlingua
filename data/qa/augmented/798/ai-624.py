import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Derive output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#2672D1',
    text=values,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    ),
    cliponaxis=False
))

# Build title and subtitle string
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    if title_text:
        title_text += "<br>"
    title_text += f"<sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=14, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    bargap=0.3,
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 700],
        dtick=100,
        showgrid=True,
        gridcolor='#EAEAEA',
        zeroline=False,
        linecolor='black',
        tickfont=dict(size=12),
        title_standoff=15
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper", yref="paper",
            x=1.0, y=-0.22,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=12, color="grey")
        )
    ]
)

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")