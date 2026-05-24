import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
    
# Derive the output filename from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data and texts from the configuration
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for plotting
categories = [item['category'] for item in chart_data]
values = [item['value'] / 100.0 for item in chart_data] # Convert percentages to decimals for Plotly

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    name='' # Hide trace name from hover
))

# Build title string
title_text = ""
if texts.get("title"):
    title_text += f"<span style='font-size: 24px;'><b>{texts['title']}</b></span>"
if texts.get("subtitle"):
    title_text += f"<br><span style='font-size: 16px;'>{texts['subtitle']}</span>"

# Update layout
fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    title_y=0.95,
    title_xanchor='left',
    title_yanchor='top',
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    yaxis=dict(
        tickformat=".0%",
        range=[0, 0.82],
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=True,
        zerolinecolor='lightgrey'
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=True,
        zerolinecolor='lightgrey'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=90, r=40, t=100, b=80)
)

# Generate and save the image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)