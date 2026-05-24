import sys
import json
import plotly.graph_objects as go

# Ensure the script is called with a single argument: the JSON file path
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Derive the output PNG filename from the input JSON filename
# e.g., 'path/to/chart.json' -> 'path/to/chart.png'
if '.' in json_path:
    base_filename = json_path.rsplit('.', 1)[0]
else:
    base_filename = json_path
output_filename = f"{base_filename}.png"

# Load chart specifications from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON in '{json_path}': {e}")
    sys.exit(1)

# Extract data, texts, colors, and other settings from the config
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', {})
shapes = config.get('shapes', [])
axis_ranges = config.get('axis_ranges', {})

# Initialize a Plotly Figure
fig = go.Figure()

# Add data series (traces) to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('name', ''),
        line=dict(
            color=colors.get('series_colors', ['#000000'])[i % len(colors.get('series_colors', ['#000000']))],
            width=3
        ),
        hoverinfo='none'
    ))

# Update the figure layout with titles, colors, axis properties, etc.
fig.update_layout(
    plot_bgcolor=colors.get('background_color'),
    paper_bgcolor=colors.get('background_color'),
    font=dict(
        family="Arial",
        size=12,
        color=colors.get('axis_color')
    ),
    xaxis=dict(
        range=axis_ranges.get('x'),
        showline=True,
        linewidth=2,
        linecolor=colors.get('axis_color'),
        zeroline=False,
        showgrid=False,
        tickvals=[-3, -2, -1, 0, 1],
        ticktext=['-3', '-2', '-1', '0', '1']
    ),
    yaxis=dict(
        range=axis_ranges.get('y'),
        showline=True,
        linewidth=2,
        linecolor=colors.get('axis_color'),
        zeroline=False,
        showgrid=False,
        tickvals=[1, 2, 3, 4, 5, 6],
        ticktext=['1', '2', '3', '4', '5', '6']
    ),
    showlegend=False,
    margin=dict(l=30, r=20, t=20, b=30),
    shapes=shapes
)

# Generate and save the chart as a high-resolution PNG file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)