import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and settings from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series specified in the JSON
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None
    ))

# Construct the title string from title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Configure the layout of the chart
fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font_family="Arial",
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        type='category',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 6000000],
        tickvals=[0, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000],
        showgrid=True,
        gridcolor='#cccccc',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=80, b=50)
)

# Determine the output filename from the input JSON filename
output_filename = pathlib.Path(json_path).stem + ".png"

# Write the chart to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")