import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Define the output image path based on the JSON filename
output_image_path = json_file_path.with_suffix(".png")

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)

# Create a figure
fig = go.Figure()

# Add a bar trace for each series from the JSON data
categories = chart_data['chart_data']['categories']
series_list = chart_data['chart_data']['series']
colors = chart_data['colors']

for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['data'],
        name=series['name'],
        marker_color=colors[i]
    ))

# Update the layout of the chart
texts = chart_data['texts']

fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    barmode='group',
    plot_bgcolor='white',
    paper_bgcolor='#F0F0F0',
    font=dict(
        family="Arial",
        size=12
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickangle=-45,
        showgrid=False,
        showline=True,
        linecolor='lightgray'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 160],
        dtick=20,
        showgrid=True,
        gridcolor='lightgray'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=60, r=40, t=80, b=150)
)

# Save the chart as a PNG image
try:
    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)