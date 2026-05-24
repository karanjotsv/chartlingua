import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get("x"),
        y=series.get("y"),
        name=series.get("name"),
        mode='lines',
        line=dict(color=colors[i] if i < len(colors) else None)
    ))

# Combine title and subtitle if they exist
title_text = texts.get("title")
if texts.get("subtitle"):
    title_text = f"{title_text}<br><sub>{texts.get('subtitle')}</sub>"

# Update layout
fig.update_layout(
    title_text=title_text,
    xaxis_title=texts.get("x_axis_title"),
    yaxis_title=texts.get("y_axis_title"),
    legend_title_text=texts.get("legend_title"),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=50, t=50, b=80),
    xaxis=dict(
        showgrid=True,
        gridcolor='#e5e5e5',
        showline=False,
        zeroline=False
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e5e5e5',
        showline=False,
        zeroline=False,
        range=[0, 57000] # Set range to avoid top line touching edge
    )
)

# Determine output filename from JSON path
filename_base = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have 'kaleido' installed (`pip install kaleido`)")
    sys.exit(1)