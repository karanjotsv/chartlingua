import sys
import json
import plotly.graph_objects as go
import os

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

# Initialize figure
fig = go.Figure()

# Add traces
for i, series in enumerate(chart_data['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        name=series['name'],
        line=dict(
            color=chart_data['colors'][i],
            dash=series['line_style']
        )
    ))

# Build title and source strings
title_text = chart_data['texts'].get('title', '')
if chart_data['texts'].get('subtitle'):
    title_text += f"<br><sub>{chart_data['texts']['subtitle']}</sub>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title=chart_data['texts']['x_axis_title'],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=False,
        tickmode='array',
        tickvals=[i * 0.001 for i in range(11)],
        ticktext=['' for _ in range(11)],
        ticks='outside',
        range=[0, 0.0105]
    ),
    yaxis=dict(
        title=chart_data['texts']['y_axis_title'],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridcolor='lightgray',
        tickmode='array',
        tickvals=[0, 0.5, 1, 1.5, 2, 2.5],
        ticktext=['0', '0,5', '1', '1,5', '2', '2,5'],
        range=[0, 2.5]
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=50, b=60),
    annotations=chart_data.get('annotations', []),
    shapes=chart_data.get('shapes', [])
)

# Determine output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")