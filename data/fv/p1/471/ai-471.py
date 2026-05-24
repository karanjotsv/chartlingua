import sys
import json
import os
import plotly.graph_objects as go

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data for plotting
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Create the figure
fig = go.Figure()

# Add traces from the JSON data
for i, series in enumerate(data_series):
    fig.add_trace(go.Bar(
        x=series.get('x', []),
        y=series.get('y', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None
    ))

# Update layout
fig.update_layout(
    title_text=texts.get('title', ''),
    title_x=0.5,
    xaxis_title_text=texts.get('x_axis_title', ''),
    yaxis_title_text=texts.get('y_axis_title', ''),
    font=dict(
        family="Arial",
        size=16
    ),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        type='category',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=False,
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        range=[0, 500],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor='lightgray',
        tickfont=dict(size=14)
    ),
    margin=dict(l=90, r=40, b=80, t=100)
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the image to a file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as '{output_filename}'")