import sys
import json
import plotly.graph_objects as go
import os

# Ensure a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Load data and settings from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure by iterating through the chart data
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get("x"),
        y=series.get("y"),
        name=series.get("name", ""),
        marker_color=colors[i % len(colors)],
        marker_line=dict(color='black', width=0.5) # Emulate border
    ))

# Construct the title string, handling potential null values
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout based on JSON data
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[25500, 29000],
        dtick=500,
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=80, b=50, l=50, r=50) # Adjust margins for title and labels
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")