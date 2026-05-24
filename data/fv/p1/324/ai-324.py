import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Create figure with subplots
fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

# Add left pie chart
if len(chart_data) > 0 and len(colors) > 0:
    fig.add_trace(go.Pie(
        labels=chart_data[0]['labels'],
        values=chart_data[0]['values'],
        marker_colors=colors[0],
        name='NatGas',
        sort=False
    ), 1, 1)

# Add right pie chart
if len(chart_data) > 1 and len(colors) > 1:
    fig.add_trace(go.Pie(
        labels=chart_data[1]['labels'],
        values=chart_data[1]['values'],
        marker_colors=colors[1],
        name='Coal',
        sort=False
    ), 1, 2)

# Update traces settings
fig.update_traces(
    textinfo='none',
    hoverinfo='label+percent',
    insidetextorientation='radial'
)

# Update layout
fig.update_layout(
    font_family="Arial",
    width=1200,
    height=500,
    margin=dict(t=100, b=40, l=40, r=400),
    showlegend=True,
    legend=dict(
        x=1,
        y=0.5,
        xanchor='left',
        yanchor='middle',
        font=dict(size=12),
        bgcolor='rgba(255,255,255,0)',
        bordercolor='rgba(0,0,0,0)',
        borderwidth=0
    ),
    annotations=[
        dict(
            text=texts.get('title_left', ''),
            align='center',
            showarrow=False,
            xref='paper', yref='paper',
            x=0.22, y=1.05,
            xanchor='center', yanchor='bottom',
            font=dict(size=16)
        ),
        dict(
            text=texts.get('title_right', ''),
            align='center',
            showarrow=False,
            xref='paper', yref='paper',
            x=0.78, y=1.05,
            xanchor='center', yanchor='bottom',
            font=dict(size=16)
        )
    ]
)

# Determine output filename
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")