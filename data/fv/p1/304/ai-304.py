import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read the JSON data from the file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)


# Extract data and texts from the JSON structure
chart_data = chart_info['chart_data'][0]
texts = chart_info['texts']
colors = chart_info['colors']

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=chart_data['labels'],
    values=chart_data['values'],
    text=chart_data['custom_text'],
    textinfo='text',
    textposition='outside',
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    insidetextorientation='horizontal'
))

# Update the layout for a clean and accurate presentation
# The 3D effect from the original is not standard in Plotly and often discouraged; a 2D pie is created instead.
# Text labels are placed outside for clarity, which is a robust choice even if the original had mixed placement.
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sup>{texts['subtitle']}</sup>"

fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    title_font_size=20,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=60, r=60, t=100, b=60),
    legend=dict(
        traceorder='normal'
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    uniformtext_minsize=10,
    uniformtext_mode='hide'
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved successfully to '{output_image_path}'")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)