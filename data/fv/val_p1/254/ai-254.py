import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])

# Check if the provided path is a file
if not json_file_path.is_file():
    print(f"Error: File not found at '{json_file_path}'")
    sys.exit(1)

# Read the JSON data from the file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_file_path}'")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Create the figure object
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    marker_line_color='black',
    marker_line_width=1,
    name='' # Hide trace name from hover
))

# Configure the layout
fig.update_layout(
    font_family="Arial",
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    plot_bgcolor='white',
    showlegend=False,
    bargap=0.1,
    margin=dict(l=90, r=20, t=20, b=80),
    title_x=0.05
)

# Customize axes to match the original chart
fig.update_xaxes(
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    ticks='outside',
    tickmode='linear',
    dtick=1,
    tickangle=0
)

fig.update_yaxes(
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    showgrid=True,
    gridwidth=1,
    gridcolor='lightgray',
    range=[0, 300000],
    tick0=0,
    dtick=50000
)

# Determine the output filename from the input JSON filename
output_filename_base = json_file_path.stem
output_image_path = f"{output_filename_base}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")