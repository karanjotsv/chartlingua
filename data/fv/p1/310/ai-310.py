import sys
import json
import os
import plotly.graph_objects as go

# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python this_script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and text from the loaded JSON
chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
categories = chart_data.get('categories', [])
series_data = chart_data.get('series', [])

# Initialize the figure
fig = go.Figure()

# Add bar traces for each series in the data
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('values', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None
    ))

# Construct the title string with HTML for styling
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the layout of the chart
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_font_size=20,
    font=dict(family="Arial"),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[25500, 29000],
        dtick=500,
        showgrid=True,
        gridcolor='lightgrey',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=80, b=60)
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to '{output_filename}'")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)