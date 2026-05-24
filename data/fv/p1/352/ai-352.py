import sys
import json
import os
import plotly.graph_objects as go

# Check if a command-line argument is provided
if len(sys.argv) < 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data from the JSON object
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Create a new figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('name', ''),
        line=dict(color=colors[i % len(colors)]) if colors else {}
    ))

# Build combined title string
title_text = texts.get('title', '')
if texts.get('source'):
    title_text += f"<br><sup>{texts.get('source')}</sup>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    xaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        showline=True,
        linecolor='black',
        mirror=True,
        range=[0, 102],
        tickmode='linear',
        tick0=1,
        dtick=2
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        showline=True,
        linecolor='black',
        mirror=True,
        range=[0, 10],
        tickmode='linear',
        tick0=0,
        dtick=1
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=100, b=80)
)

# Determine output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_image_path, scale=2)
    print(f"Chart successfully saved to {output_image_path}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)