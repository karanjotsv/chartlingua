import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at '{json_path}'")
    sys.exit(1)

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data and settings from the JSON structure
chart_data = chart_config.get('chart_data', [])
trendlines = chart_config.get('trendlines', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add scatter plot traces for the main data
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)] if colors else '#000000'
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='markers',
        name=series.get('name'),
        marker=dict(color=color, size=8, line=dict(width=0)),
        showlegend=True
    ))

# Add line traces for the trendlines
for i, line in enumerate(trendlines):
    color = colors[i % len(colors)] if colors else '#000000'
    fig.add_trace(go.Scatter(
        x=line.get('x'),
        y=line.get('y'),
        mode='lines',
        name=line.get('name'),
        line=dict(color=color, width=3),
        showlegend=False
    ))

# Configure the chart layout
fig.update_layout(
    font=dict(family="Arial", size=18, color="black"),
    plot_bgcolor='white',
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    xaxis=dict(
        autorange='reversed',
        range=[-24.5, -17],
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        ticks='inside',
        tickwidth=2,
        ticklen=6,
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        range=[1.6, 2.8],
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        ticks='inside',
        tickwidth=2,
        ticklen=6,
        showgrid=False,
        zeroline=False
    ),
    legend=dict(
        x=0.95,
        y=0.35,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    margin=dict(l=90, r=30, t=30, b=80)
)

# Add title if it exists in the JSON
title_text = texts.get('title')
if title_text:
    fig.update_layout(title_text=title_text, title_x=0.5)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to '{output_filename}'")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)