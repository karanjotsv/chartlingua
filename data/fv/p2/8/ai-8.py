import sys
import os
import json
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load the chart data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

# Extract data and texts from the JSON structure
chart_data = chart_spec.get('chart_data', [])
texts = chart_spec.get('texts', {})
colors = chart_spec.get('colors', [])

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]
slice_texts = [d['text'] for d in chart_data]

# --- Create the Plotly Figure ---

fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=slice_texts,
    marker=dict(colors=colors),
    pull=[0.08, 0.08, 0.08],  # To create the exploded effect
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    rotation=-15,  # Adjust start angle to match the original chart
    texttemplate='%{text}',
    textposition='inside',
    insidetextorientation='radial',
    insidetextfont=dict(
        family="Arial",
        size=18,
        color="black"
    )
))

# --- Update Layout and Styling ---

# Construct title and source strings
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# The original chart has no visible title, source, or legend
# The logic is kept for robustness with other JSON files
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_font=dict(family="Arial"),
    showlegend=False,
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(family="Arial"),
    margin=dict(t=20, b=20, l=20, r=20)
)

# --- Output the image ---

# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved as {output_image_path}")