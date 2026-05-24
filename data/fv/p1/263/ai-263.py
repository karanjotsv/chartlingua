import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data from the loaded JSON
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])
shapes = chart_data.get('shapes', [])

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        name=series.get('name', ''),
        line=dict(color=colors[i % len(colors)], width=3),
        showlegend=False
    ))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=14),
    xaxis_title=texts.get('x_axis_title', ''),
    yaxis_title=texts.get('y_axis_title', ''),
    xaxis_title_font_size=20,
    yaxis_title_font_size=20,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=50, t=50, b=220),
    shapes=shapes,
    annotations=texts.get('annotations', []),
    showlegend=False
)

# Configure axes styling
axis_color = "#4C72B0"
fig.update_xaxes(
    showline=True,
    linewidth=2,
    linecolor=axis_color,
    mirror=False,
    showgrid=False,
    zeroline=False,
    showticklabels=False,
    range=[-5, 95]
)

fig.update_yaxes(
    showline=True,
    linewidth=2,
    linecolor=axis_color,
    mirror=False,
    showgrid=False,
    zeroline=False,
    showticklabels=False,
    range=[-15, 120]
)

# Generate the output filename from the input JSON path
output_filename = json_file_path.stem + ".png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)