import sys
import json
import os
import plotly.graph_objects as go

# Ensure a command-line argument is provided for the JSON file path
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON data file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series in the JSON
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        showlegend=False
    ))

# Combine title and subtitle using HTML for rich text formatting
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the layout of the chart to match the original image
fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20}
    },
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        type='category',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=False
    ),
    yaxis=dict(
        range=[0, 250],
        tickvals=[0, 50, 100, 150, 200, 250],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor='darkgrey',
        gridwidth=1
    ),
    margin=dict(l=90, r=40, t=100, b=80),
    showlegend=False
)

# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the figure to a high-resolution PNG image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")