import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    hoverinfo='label+percent',
    textinfo='none',
    sort=False,  # This is crucial to preserve the order from the JSON file
    direction='clockwise'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout
title_text = texts.get('title')
fig.update_layout(
    title=dict(
        text=title_text if title_text else '',
        x=0.5,
        font=dict(
            family="Arial",
            size=18
        )
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=True,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=80, b=40, l=40, r=40),
    width=800,
    height=550
)

# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)