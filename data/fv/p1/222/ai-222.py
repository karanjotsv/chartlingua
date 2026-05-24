import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get("chart_data", {})
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
categories = chart_data.get("categories", [])
series_data = chart_data.get("series", [])

if not series_data:
    print("Error: 'series' data is missing in the JSON file.")
    sys.exit(1)

values = series_data[0].get("values", [])

# Create the pie chart trace
pie_trace = go.Pie(
    labels=categories,
    values=values,
    marker=dict(colors=colors),
    textinfo='percent',
    textposition='outside',
    hoverinfo='label+percent',
    sort=False,
    insidetextorientation='radial'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Build the title string
title_text = texts.get("title", "")
subtitle_text = texts.get("subtitle", "")
if subtitle_text:
    title_text = f"{title_text}<br>{subtitle_text}"

# Update the layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='#e9e7f5',
    paper_bgcolor='#e9e7f5',
    margin=dict(t=100, b=100, l=40, r=40)
)

# Generate the output filename from the input JSON filename
base_filename, _ = os.path.splitext(os.path.basename(json_path))
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have 'kaleido' installed (`pip install kaleido`) for static image export.")
    sys.exit(1)