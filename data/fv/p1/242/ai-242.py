import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('name', f'Series {i+1}'),
        line=dict(color=colors[i] if i < len(colors) else None, width=2)
    ))

# Construct title and source strings using HTML for line breaks
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        range=[0, 10],
        tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 100.5],
        tickvals=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    showlegend=False,
    plot_bgcolor='white',
    margin=dict(l=100, r=30, t=50, b=80),
    width=800,
    height=600
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)