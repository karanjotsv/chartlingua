import sys
import json
import os
import plotly.graph_objects as go

# Check if the JSON file path is provided
if len(sys.argv) < 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_filepath = sys.argv[1]

# Read the JSON data file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_filepath}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(
    go.Bar(
        x=categories,
        y=values,
        marker_color=colors[0],
        name='',  # Hide legend entry for single series
        marker_line_width=0
    )
)

# Combine title and subtitle if available
title_text = texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout for a professional look and feel
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    yaxis_title=texts['y_axis_title'],
    xaxis_title=texts['x_axis_title'],
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        tickangle=-90,
        showline=False,
        linecolor='black'
    ),
    yaxis=dict(
        range=[0, 50],
        dtick=5,
        showgrid=True,
        gridcolor='LightGray',
        showline=True,
        linecolor='black'
    ),
    margin=dict(l=80, r=40, t=80, b=120)
)

# Generate the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_filepath))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")