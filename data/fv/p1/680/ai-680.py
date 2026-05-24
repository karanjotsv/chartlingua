import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the parsed JSON
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create a figure with 3 rows of subplots
fig = make_subplots(
    rows=3, cols=1,
    subplot_titles=(texts['title_1'], texts['title_2'], texts['title_3']),
    vertical_spacing=0.18
)

# Add the first trace (Flight Angle)
fig.add_trace(go.Scatter(
    x=chart_data[0]['x_values'],
    y=chart_data[0]['y_values'],
    mode='lines',
    line=dict(color=colors[0], shape='spline', smoothing=0.7),
    showlegend=False
), row=1, col=1)

# Add the second trace (Velocity)
fig.add_trace(go.Scatter(
    x=chart_data[1]['x_values'],
    y=chart_data[1]['y_values'],
    mode='lines',
    line=dict(color=colors[0], shape='spline', smoothing=1.0),
    showlegend=False
), row=2, col=1)

# Add the third trace (Flight Trajectory)
fig.add_trace(go.Scatter(
    x=chart_data[2]['x_values'],
    y=chart_data[2]['y_values'],
    mode='lines',
    line=dict(color=colors[0], shape='spline', smoothing=0.8),
    showlegend=False
), row=3, col=1)

# Update the axis titles for each subplot
fig.update_xaxes(title_text=texts['x_axis_title_1'], row=1, col=1)
fig.update_yaxes(title_text=texts['y_axis_title_1'], row=1, col=1)
fig.update_xaxes(title_text=texts['x_axis_title_2'], row=2, col=1)
fig.update_yaxes(title_text=texts['y_axis_title_2'], row=2, col=1)
fig.update_xaxes(title_text=texts['x_axis_title_3'], row=3, col=1)
fig.update_yaxes(title_text=texts['y_axis_title_3'], row=3, col=1)

# Apply global layout settings
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    height=700,
    width=800,
    margin=dict(l=80, r=40, t=60, b=50)
)

# Style all axes to match the original image (black lines, no grid)
fig.update_xaxes(
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    ticks='outside',
    showgrid=False
)
fig.update_yaxes(
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    ticks='outside',
    showgrid=False
)

# Determine the output filename from the input JSON path
output_filename = pathlib.Path(json_path).stem + '.png'

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")