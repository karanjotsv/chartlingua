import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

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

# Extract data and texts
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])
line_color = colors[0] if colors else '#000000'

# Create subplots
fig = make_subplots(rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.2,
                    subplot_titles=(texts.get("title_top"), texts.get("title_bottom")))

# Add trace for the top plot
fig.add_trace(go.Scatter(
    x=chart_data[0]['x_values'],
    y=chart_data[0]['y_values'],
    mode='lines',
    line=dict(color=line_color),
    showlegend=False
), row=1, col=1)

# Add trace for the bottom plot
fig.add_trace(go.Scatter(
    x=chart_data[1]['x_values'],
    y=chart_data[1]['y_values'],
    mode='lines',
    line=dict(color=line_color),
    showlegend=False
), row=2, col=1)

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    margin=dict(t=50, r=40, b=60, l=80)
)

# Update axes for the top plot
fig.update_yaxes(
    title_text=texts.get("y_axis_label_top"),
    row=1, col=1,
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    ticks='outside',
    gridcolor='#D3D3D3',
    range=[0, 7000]
)

# Update axes for the bottom plot
fig.update_xaxes(
    title_text=texts.get("x_axis_label"),
    row=2, col=1,
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    ticks='outside',
    gridcolor='#D3D3D3',
    range=[0, 40]
)
fig.update_yaxes(
    title_text=texts.get("y_axis_label_bottom"),
    row=2, col=1,
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    ticks='outside',
    gridcolor='#D3D3D3',
    range=[-0.2, 0.2]
)

# Make sure all axes show their box
fig.update_xaxes(
    showline=True, linewidth=1, linecolor='black', mirror=True, ticks='outside',
    row=1, col=1
)

# Configure subplot titles font
for annotation in fig.layout.annotations:
    annotation.font.size = 12

# Generate output filename from the input JSON path
output_filename = json_file_path.stem + ".png"

# Save the figure
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")