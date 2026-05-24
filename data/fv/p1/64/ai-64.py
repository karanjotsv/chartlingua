import sys
import json
import os
import plotly.graph_objects as go

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read the JSON data from the file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
data = chart_data.get('chart_data', {})
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])
categories = data.get('categories', [])
series_list = data.get('series', [])

# Create a new figure
fig = go.Figure()

# Add a bar trace for each series in the data
for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        name=series.get('name', ''),
        x=series.get('values', []),
        y=categories,
        orientation='h',
        marker_color=colors[i % len(colors)]
    ))

# Update the layout of the chart
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        font=dict(family="Arial", size=18)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#D3D3D3',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False
    ),
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial"),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=300, r=30, t=80, b=80)
)

# Determine the output filename from the input JSON path
base_filename, _ = os.path.splitext(os.path.basename(json_path))
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)