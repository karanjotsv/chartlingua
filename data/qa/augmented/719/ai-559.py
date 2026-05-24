import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the loaded configuration
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_values = [f'{v:,}'.replace(',', ' ') for v in values]

# Create the Plotly figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#297ACC',
    text=text_values,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Build title string
title_text = ""
if texts.get("title"):
    title_text += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>'

# Configure layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linecolor='lightgray',
        tickfont=dict(family="Arial", size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 150000],
        gridcolor='lightgray',
        tickfont=dict(family="Arial", size=12),
        tickformat=',.0f'
    ),
    plot_bgcolor='white',
    showlegend=False,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=90, r=40, t=60, b=120),
    annotations=[]
)

# Add source annotation
source_text = ""
if texts.get("source"):
    source_text += texts["source"]
if texts.get("note"):
    source_text += f'<br>{texts["note"]}'

if source_text:
    fig.add_annotation(
        text=source_text,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.2, # Adjust this value to position the source text correctly below the x-axis
        xanchor='right',
        yanchor='top',
        font=dict(family="Arial", size=12)
    )

# Determine output filename and save the image
output_path = Path(json_path).with_suffix('.png')
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")