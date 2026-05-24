import sys
import json
import os
import plotly.graph_objects as go

# Ensure a single command-line argument is provided for the JSON file path
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Read and decode the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly pie chart
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    textinfo='percent',
    hoverinfo='label+percent',
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise',
    rotation=-40, # Adjust rotation to match the original chart's starting point
    textfont=dict(
        color='black',
        size=14
    ),
    insidetextorientation='horizontal'
))

# Format the title string
title_text = f"<b>{texts.get('title', '')}</b>"

# Update layout for styling, title, legend, and margins
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.98,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=20)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.92,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=50, r=50, t=120, b=50),
    paper_bgcolor='white'
)

# Write the image to a file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)