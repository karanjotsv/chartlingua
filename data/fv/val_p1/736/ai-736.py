import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_filepath = sys.argv[1]

# Read data from JSON file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_filepath}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_filepath}' is not a valid JSON file.")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data lists for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else '#375E97',
    text=values,
    textposition='inside',
    textangle=-90,
    textfont=dict(color='white', size=12, family='Arial'),
    insidetextanchor='middle'
))

# Configure layout
fig.update_layout(
    title=dict(
        text=texts.get('title', ''),
        x=0.5,
        xanchor='center',
        font=dict(size=24)
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        type='category' # Ensures all categories are shown
    ),
    yaxis=dict(
        visible=False
    ),
    plot_bgcolor='#E9E9E9',
    paper_bgcolor='#E9E9E9',
    showlegend=False,
    margin=dict(t=80, b=50, l=40, r=40)
)

# Determine output filename from input JSON path
base_name = Path(json_filepath).stem
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")