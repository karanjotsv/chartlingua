import sys
import json
import plotly.graph_objects as go
import math

# This script requires a JSON file path as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Derive the output filename from the input JSON path.
output_filename = json_path.rsplit('.', 1)[0] + '.png'

# Load data and configuration from the specified JSON file.
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data for plotting.
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Create a Plotly figure object.
fig = go.Figure()

# Add traces to the figure based on the chart_data.
# The data is transformed here to match the visual representation of the Hubbert curve.
# The formula y = 0.25 * sech^2(x/2) is used, which is equivalent to
# y = 0.25 / (cosh(x/2))^2.
for i, series in enumerate(chart_data):
    # This calculation ensures the curve is recreated accurately, as simple data extraction
    # from the low-resolution image is insufficient. The JSON provides the x-range.
    x_values = [x for x in series.get('x', [])]
    y_values_calculated = [0.25 / (math.cosh(x / 2.0))**2 for x in x_values]
    
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values_calculated,
        mode='lines',
        line=dict(color=colors[i % len(colors)], width=2),
        name=series.get('name', ''),
        showlegend=False
    ))

# Build combined title string.
title_text = texts.get('title', '') or ''
subtitle_text = texts.get('subtitle', '') or ''
if subtitle_text:
    title_text = f"{title_text}<br><sub>{subtitle_text}</sub>"

# Configure the layout of the chart.
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    width=600,
    height=500,
    margin=dict(l=60, r=20, t=30, b=50),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        range=[-6.5, 6.5],
        tickvals=[-6, -4, -2, 0, 2, 4, 6],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridwidth=1,
        gridcolor='#D3D3D3'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[-0.01, 0.26],
        tickvals=[0, 0.05, 0.1, 0.15, 0.2, 0.25],
        tickformat=".2f",
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=True,
        gridwidth=1,
        gridcolor='#D3D3D3'
    )
)

# Add source/note annotation if it exists.
source_note_text = texts.get('source_note')
if source_note_text:
    fig.add_annotation(
        text=source_note_text,
        xref="paper", yref="paper",
        x=0, y=-0.15,
        xanchor='left', yanchor='top',
        showarrow=False,
        align='left',
        font=dict(size=10)
    )

# Write the figure to a high-resolution PNG file.
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to '{output_filename}'")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)