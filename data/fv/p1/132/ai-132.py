import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and text from the loaded JSON
data_series = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
categories = [item.get('category', '') for item in data_series]
num_series = len(texts.get('legend_labels', []))
series_values = [[item.get('values', [None]*num_series)[i] for item in data_series] for i in range(num_series)]

# Create the figure
fig = go.Figure()

# Add a bar trace for each series
for i in range(num_series):
    fig.add_trace(go.Bar(
        name=texts['legend_labels'][i],
        x=categories,
        y=series_values[i],
        marker_color=colors[i]
    ))

# Build title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    title_y=0.95,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12),
    barmode='group',
    plot_bgcolor='white',
    legend=dict(
        x=0.75,
        y=0.5,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    margin=dict(l=60, r=40, t=100, b=150),
    yaxis=dict(
        range=[0, 80],
        tickmode='linear',
        tick0=0,
        dtick=10,
        gridcolor='#e0e0e0'
    ),
    xaxis=dict(
        tickangle=-45
    )
)

# Show axis lines
fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
fig.update_yaxes(showline=True, linewidth=1, linecolor='black')

# Generate and save the image
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")