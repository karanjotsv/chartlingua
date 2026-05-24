import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Ensure the file exists before proceeding
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure
if chart_data:
    series = chart_data[0] # Assuming a single series bar chart
    x_values = [item['x'] for item in series['data']]
    y_values = [item['y'] for item in series['data']]
    
    fig.add_trace(go.Bar(
        x=x_values,
        y=y_values,
        marker_color=colors[0] if colors else None,
        name=series.get("series_name", "")
    ))

# Combine title and subtitle if available
title_text = texts.get("title", "")
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        type='category',
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        range=[0, 120],
        tick0=0,
        dtick=20,
        gridcolor='grey',
        linecolor='black'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=80, b=80)
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")