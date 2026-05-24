import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for the chart
chart_data = config.get('chart_data', [])
colors = config.get('colors', [])

# Prepare data for Plotly Pie chart
labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
pie_texts = [f"{d['label']}<br>{d['value']:.2f}%" for d in chart_data]
pull_values = [0.1 if d['label'] == 'Mozilla Firefox' else 0 for d in chart_data]

# Create the pie chart figure
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    text=pie_texts,
    hoverinfo='label+percent',
    textinfo='text',
    textfont=dict(
        family="Arial",
        size=16,
        color='white'
    ),
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=2)
    ),
    pull=pull_values,
    sort=False,
    direction='clockwise',
    rotation=75
)])

# Update layout properties
fig.update_layout(
    showlegend=False,
    paper_bgcolor='black',
    plot_bgcolor='black',
    margin=dict(l=20, r=20, t=20, b=20),
    font=dict(family="Arial")
)

# Set text position to be inside the slices
fig.update_traces(textposition='inside', insidetextorientation='radial')

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Write the figure to a PNG image file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)