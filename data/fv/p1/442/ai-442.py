import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = sys.argv[1]

# Read the JSON data
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data from the JSON object
chart_data = chart_info.get('chart_data', [])
colors_data = chart_info.get('colors', {})
slice_colors = colors_data.get('slices', [])
text_colors = colors_data.get('texts', [])

# Prepare data for Plotly
labels = [item.get('category') for item in chart_data]
values = [item.get('value') for item in chart_data]
slice_texts = [f"{item.get('category')}<br>{item.get('value')}%" for item in chart_data]

# Create the donut chart trace
donut_trace = go.Pie(
    labels=labels,
    values=values,
    hole=0.4,
    marker=dict(colors=slice_colors),
    text=slice_texts,
    textinfo='text',
    textposition='inside',
    insidetextfont=dict(
        family='Arial',
        size=22,
        color=text_colors
    ),
    hoverinfo='none',
    sort=False,
    direction='clockwise',
    rotation=90
)

# Create the layout
layout = go.Layout(
    showlegend=False,
    paper_bgcolor='#000000',
    plot_bgcolor='#000000',
    margin=dict(l=20, r=20, t=20, b=20),
    font=dict(family="Arial")
)

# Create the figure
fig = go.Figure(data=[donut_trace], layout=layout)

# Generate the output filename and save the image
output_filename = pathlib.Path(json_file_path).with_suffix('.png')
fig.write_image(output_filename, scale=2, width=600, height=600)

print(f"Chart saved to {output_filename}")