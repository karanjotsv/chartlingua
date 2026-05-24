import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces (bars) to the figure
for i, series in enumerate(chart_data):
    # Format bar labels with spaces as thousand separators
    bar_labels = [f'{val:,}'.replace(',', ' ') for val in series.get('y', [])]
    
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None,
        text=bar_labels,
        textposition='inside',
        textangle=-90,
        insidetextanchor='end',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        hoverinfo='none'
    ))

# Update layout of the figure
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        font=dict(size=18)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_standoff=10,
        showgrid=True,
        gridcolor='lightgrey',
        range=[1000000, 1800000],
        dtick=100000,
        tickformat=' ' # Use space as thousand separator
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=100, b=50),
    annotations=texts.get('annotations', [])
)

# Determine the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")